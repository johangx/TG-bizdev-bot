import asyncio
import time
import random
import re
import gspread
from telethon import TelegramClient
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.errors import FloodWaitError, PeerFloodError, UserPrivacyRestrictedError
from telethon.tl import functions
from google.oauth2.service_account import Credentials

# === CONFIGURATION ===
api_id = 24967410
api_hash = 'a772e39631b4b245de2b0fafd1850a71'
session_name = 'admin_dm_session'

# Google Sheets setup
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

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
            'contacts': []
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
    
    # Remove duplicates
    unique_contacts = list(set(contacts))
    
    if unique_contacts:
        print(f"\n✅ Total contacts found: {len(unique_contacts)}")
        print(f"Contacts: {unique_contacts}")
    else:
        print(f"\n❌ No contacts found for {username}")
    
    return {
        'channel': username,
        'contacts': unique_contacts
    }

async def main():
    """Main function"""
    client = TelegramClient(session_name, api_id, api_hash)
    
    try:
        await client.start()
        print("✅ Successfully connected to Telegram!")
        
        # Connect to Google Sheets
        credentials = Credentials.from_service_account_file(
            'service_account.json', scopes=SCOPES
        )
        
        gc = gspread.authorize(credentials)
        spreadsheet_id = '19IuLIlAOlzoiiqY4S55tG8PHkzupPauvCGfX0VvcfK0'
        
        # Open the "Tech" tab
        try:
            sheet = gc.open_by_key(spreadsheet_id).worksheet("Tech")
            print("✅ Successfully connected to 'Tech' tab!")
        except Exception as e:
            print(f"❌ Error accessing 'Tech' tab: {e}")
            return
        
        # Read all data from the Tech tab
        all_data = sheet.get_all_values()
        
        # Find channels in column B (index 1)
        channels_to_process = []
        for i, row in enumerate(all_data, 1):
            if len(row) > 1 and row[1]:  # Column B has data
                link = row[1].strip()
                if 'https://t.me/' in link:
                    # Extract channel name from URL
                    channel_name = link.replace('https://t.me/', '')
                    channels_to_process.append((i, channel_name, link))
                    print(f"Row {i}: {channel_name}")
        
        print(f"\n📋 Found {len(channels_to_process)} channels to process")
        
        if not channels_to_process:
            print("❌ No channels found in column B")
            return
        
        # Process each channel
        results = []
        for i, (row_num, channel_name, link) in enumerate(channels_to_process, 1):
            print(f"\n🔄 Processing {i}/{len(channels_to_process)}: {channel_name}")
            
            # Add delay to avoid rate limits
            if i > 1:
                delay = random.uniform(2, 5)
                print(f"⏳ Waiting {delay:.1f} seconds...")
                await asyncio.sleep(delay)
            
            result = await scan_channel_for_admins(client, channel_name)
            result['row_num'] = row_num
            results.append(result)
        
        # Update Google Sheet with results
        print(f"\n📋 Updating Google Sheet...")
        
        for result in results:
            row_num = result['row_num']
            admin_data = ', '.join(result['contacts']) if result['contacts'] else 'N/A'
            
            try:
                # Update admin column (C)
                sheet.update_cell(row_num, 3, admin_data)
                print(f"✅ Row {row_num} - Admin: {admin_data}")
                
                # Add small delay to avoid rate limits
                time.sleep(0.5)
                
            except Exception as e:
                print(f"❌ Error updating row {row_num}: {e}")
                if "429" in str(e):  # Rate limit
                    print("Rate limit hit, waiting 60 seconds...")
                    time.sleep(60)
                    # Try again
                    try:
                        sheet.update_cell(row_num, 3, admin_data)
                        print(f"✅ Row {row_num} - Admin: {admin_data} (retry successful)")
                    except Exception as e2:
                        print(f"❌ Retry failed for row {row_num}: {e2}")
        
        print(f"\n🎯 **Update Complete!**")
        print(f"✅ Processed {len(results)} channels")
        print(f"✅ Updated Google Sheet 'Tech' tab column C")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())


