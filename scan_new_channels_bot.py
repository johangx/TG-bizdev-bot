import asyncio
import time
import random
import re
import csv
import gspread
from telethon import TelegramClient
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.errors import FloodWaitError, PeerFloodError, UserPrivacyRestrictedError
from telethon.tl import functions
from google.oauth2.service_account import Credentials

# === CONFIGURATION ===
api_id = 24967410  # Your Telegram API ID
api_hash = 'a772e39631b4b245de2b0fafd1850a71'  # Your Telegram API Hash
session_name = 'admin_dm_session'  # Session file name

# Google Sheets setup
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# New channels to scan (from row 64+)
new_channels = ['iamalexfalcon', 'binance_announcements', 'sergeisergienkoen', 'MoneyDogs_Community', 'pixelverse_xyz', 'tonstationgames', 'wallet_news', 'just', 'theTapCoins', 'TONKombatOfficial', 'popcorn_today', 'ToNmetasilense', 'app301', 'battle_games_com', 'findolucky', 'thememetimes', 'blumcrypto_memepad', 'Binance_Moonbix_Announcements', 'CEXIO_Announcements', 'ceosanya', 'dogiators', 'thearefcrypto', 'cheatkott', 'caps', 'buzz', 'NewsPlayToEarn', 'deckforge_official', 'boinkersNews', 'lab_trade', 'startups', 'venture', 'xdaoapp', 'trade', 'Airdrop_Fam', 'coinmarket', 'CRYPTO_jokker', 'Holdcoin_Channel', 'hash_cats', 'architecton_tech', 'tomo_cat', 'Alexnosleep', 'PiAnnouncements', 'pigscrew', 'therealyescoin', 'the_vertus', 'matchain_fam', 'ForUAI_channel', 'DejenNews', 'tabi_ann', 'sparkscircle', 'pepefrogbar', 'dealdost', 'AirdropFindTeam', 'hexnio', 'Catia_Announcement', 'CITY_Holder', 'INSIDERR_POLITIC', 'pocketfi', 'CryptoMemeFoundation', 'The_RatsKingdom', 'gameechannel', 'learn2earnings', 'cryp2day', 'livenews_1win', 'Geminstitute', 'avagoldcoin', 'farmfrog', 'grafunmeme', 'iPapkorn', 'NOTAI_ann', 'solana_now_trending', 'onus_globalchannel', 'MeshchainAi', 'alpha_feed', 'ponchiqs', 'smpl_app', 'Getmodpcs', 'theFreeDogs_ANN', 'CryptoHylos', 'boomloudcoin', 'marketmakingpro', 'CRYPTO_insidderr', 'AnuragxCricket']

def extract_contacts_from_text(text):
    """Extract Telegram usernames and contact info from text"""
    if not text:
        return []
    
    contacts = []
    
    # Find Telegram usernames (@username)
    usernames = re.findall(r'@(\w+)', text)
    contacts.extend([f"@{username}" for username in usernames])
    
    # Find common contact keywords
    contact_keywords = ['contact', 'admin', 'ads', 'buy ads', 'cooperation', 'partnership', 'business']
    lines = text.lower().split('\n')
    for line in lines:
        for keyword in contact_keywords:
            if keyword in line:
                # Extract any @username from this line
                line_usernames = re.findall(r'@(\w+)', line)
                contacts.extend([f"@{username}" for username in line_usernames])
                break
    
    return list(set(contacts))  # Remove duplicates

async def get_channel_info(client, username):
    """Get channel information including description and linked chat"""
    try:
        entity = await client.get_entity(username)
        
        # Get channel description/about
        about = ""
        try:
            full_chat = await client(functions.channels.GetFullChannelRequest(entity))
            about = full_chat.full_chat.about or ""
        except Exception as e:
            print(f"  Could not get full channel info: {e}")
        
        return entity, about
    except Exception as e:
        print(f"  Could not access {username}: {e}")
        return None, ""

async def get_group_admins(client, entity):
    """Get admins from a group/supergroup"""
    try:
        admins = []
        async for admin in client.iter_participants(entity, filter=ChannelParticipantsAdmins):
            if not getattr(admin, 'bot', False) and not getattr(admin, 'is_self', False):
                if admin.username:
                    admins.append(f"@{admin.username}")
                else:
                    admins.append(admin.first_name or "Unknown")
        return admins
    except Exception as e:
        print(f"  Could not fetch admins: {e}")
        return []

async def scan_channel_for_admins(client, username):
    """Scan a single channel for admin information"""
    print(f"\n{'='*50}")
    print(f"Processing channel: {username}")
    print(f"{'='*50}")
    
    entity, description = await get_channel_info(client, username)
    if not entity:
        return {
            'channel': username,
            'contacts': [],
            'community_links': []
        }
    
    print(f"Channel: {entity.title}")
    if description:
        print(f"Description: {description}")
    
    # Extract contacts from description
    contacts = extract_contacts_from_text(description)
    if contacts:
        print(f"Contacts found in description: {contacts}")
    
    # Try to get admins directly
    print("\nTrying to get admins from channel...")
    try:
        admins = await get_group_admins(client, entity)
        if admins:
            print(f"✅ Direct admins found: {admins}")
            contacts.extend(admins)
    except Exception as e:
        print(f"  Could not fetch admins: {e}")
    
    community_links = []
    
    # If no contacts found, scan posts for community groups
    if not contacts:
        print(f"❌ No contacts found for {username}")
        print(f"Scanning all posts in {username} for group/community links...")
        
        group_keywords = ['chat', 'group', 'community', 'discussion', 'support', 'help']
        found_group_links = set()
        
        try:
            async for message in client.iter_messages(entity, limit=None):
                if message and message.text:
                    # Find t.me links
                    tme_links = re.findall(r'https://t\.me/(\w+)', message.text)
                    for link in tme_links:
                        # Check if link contains group-related keywords
                        if any(keyword in link.lower() for keyword in group_keywords):
                            found_group_links.add(link)
            
            if found_group_links:
                print(f"Found group/community links in posts: {list(found_group_links)}")
                
                # Filter links to only include those similar to the channel name
                filtered_group_links = [
                    link for link in found_group_links
                    if username.lower() in link.lower()
                ]
                
                if filtered_group_links:
                    print(f"Filtered group links: {filtered_group_links}")
                    
                    # Try to get admins from community groups
                    for group_link in filtered_group_links[:2]:  # Limit to first 2
                        try:
                            print(f"    Fetching admins for group: {group_link}")
                            group_entity = await client.get_entity(group_link)
                            group_admins = await get_group_admins(client, group_entity)
                            if group_admins:
                                print(f"    Group admins found: {len(group_admins)}")
                                for admin in group_admins:
                                    print(f"      - {admin}")
                                contacts.extend(group_admins)
                                community_links.append(f"https://t.me/{group_link}")
                            else:
                                print(f"    No admins found for group: {group_link}")
                        except Exception as e:
                            print(f"    Could not get group entity for {group_link}: {e}")
        except Exception as e:
            print(f"Error scanning messages: {e}")
    
    # Remove duplicates
    unique_contacts = list(set(contacts))
    unique_community_links = list(set(community_links))
    
    if unique_contacts:
        print(f"\n✅ Total contacts found: {len(unique_contacts)}")
        print(f"Contacts: {unique_contacts}")
    else:
        print(f"\n❌ No contacts found for {username}")
    
    return {
        'channel': username,
        'contacts': unique_contacts,
        'community_links': unique_community_links
    }

async def main():
    """Main function"""
    client = TelegramClient(session_name, api_id, api_hash)
    
    try:
        await client.start()
        print("✅ Successfully connected to Telegram!")
        
        print(f"📋 Found {len(new_channels)} new channels to process")
        
        # Process results
        results = []
        
        for i, username in enumerate(new_channels, 1):
            print(f"\n🔄 Processing {i}/{len(new_channels)}: {username}")
            
            # Add delay to avoid rate limits
            if i > 1:
                delay = random.uniform(2, 5)
                print(f"⏳ Waiting {delay:.1f} seconds...")
                await asyncio.sleep(delay)
            
            result = await scan_channel_for_admins(client, username)
            results.append(result)
        
        # Export results to CSV
        print(f"\n📊 Exporting results to CSV...")
        with open('new_channels_results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Broadcast Channel Link', 'Community Chat Links', 'Admins (comma-separated)']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for result in results:
                channel_link = f"https://t.me/{result['channel']}"
                community_links = '\n'.join(result['community_links']) if result['community_links'] else ''
                admins = ', '.join(result['contacts']) if result['contacts'] else ''
                
                writer.writerow({
                    'Broadcast Channel Link': channel_link,
                    'Community Chat Links': community_links,
                    'Admins (comma-separated)': admins
                })
        
        print("✅ Results exported to new_channels_results.csv")
        
        # Now update Google Sheet
        print("\n📋 Updating Google Sheet...")
        
        credentials = Credentials.from_service_account_file(
            'service_account.json', scopes=SCOPES
        )
        
        gc = gspread.authorize(credentials)
        spreadsheet_id = '19IuLIlAOlzoiiqY4S55tG8PHkzupPauvCGfX0VvcfK0'
        sheet = gc.open_by_key(spreadsheet_id).sheet1
        
        # Update rows 64 onward
        for i, result in enumerate(results):
            row_num = 64 + i
            admin_data = ', '.join(result['contacts']) if result['contacts'] else 'N/A'
            community_data = '\n'.join(result['community_links']) if result['community_links'] else 'N/A'
            
            try:
                # Update admin column (B)
                sheet.update_cell(row_num, 2, admin_data)
                print(f"✅ Row {row_num} - Admin: {admin_data}")
                
                # Update community column (C)
                sheet.update_cell(row_num, 3, community_data)
                print(f"✅ Row {row_num} - Community: {community_data}")
                
                # Add small delay to avoid rate limits
                time.sleep(0.5)
                
            except Exception as e:
                print(f"❌ Error updating row {row_num}: {e}")
                if "429" in str(e):  # Rate limit
                    print("Rate limit hit, waiting 60 seconds...")
                    time.sleep(60)
        
        print(f"\n🎯 **Update Complete!**")
        print(f"✅ Processed {len(results)} new channels")
        print(f"✅ Updated Google Sheet rows 64-{63 + len(results)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main()) 