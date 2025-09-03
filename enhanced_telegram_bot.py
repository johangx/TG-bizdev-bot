import asyncio
import time
import random
import re
import csv
from telethon import TelegramClient, functions
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.errors import FloodWaitError, PeerFloodError, UserPrivacyRestrictedError

# === CONFIGURATION ===
api_id = 24967410
api_hash = 'a772e39631b4b245de2b0fafd1850a71'
session_name = 'admin_dm_session'
channels_file = 'channels.txt'

def read_channel_usernames():
    """Read channel usernames from file"""
    with open(channels_file, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def extract_contacts_from_text(text):
    """Extract contact information from text"""
    if not text:
        return []
    
    contacts = []
    
    # Find @usernames
    usernames = re.findall(r'@(\w+)', text)
    contacts.extend([f"@{username}" for username in usernames])
    
    # Find t.me links
    tme_links = re.findall(r'https://t\.me/(\w+)', text)
    contacts.extend([f"https://t.me/{link}" for link in tme_links])
    
    # Find contact keywords
    contact_keywords = ['contact', 'admin', 'owner', 'support', 'help', 'ads', 'cooperation', 'partnership']
    lines = text.lower().split('\n')
    for line in lines:
        for keyword in contact_keywords:
            if keyword in line:
                # Extract username after keyword
                match = re.search(rf'{keyword}[:\s]*@(\w+)', line)
                if match:
                    contacts.append(f"@{match.group(1)}")
    
    return list(set(contacts))  # Remove duplicates

async def get_channel_info(client, username):
    """Get channel information including description"""
    try:
        entity = await client.get_entity(username)
        print(f"Channel: {entity.title}")
        
        # Get full channel info
        try:
            full_channel = await client(functions.channels.GetFullChannelRequest(channel=entity))
            if full_channel.full_chat.about:
                print(f"Description: {full_channel.full_chat.about}")
                return full_channel.full_chat.about
        except Exception as e:
            print(f"Could not get full channel info: {e}")
        
        return ""
    except Exception as e:
        print(f"Could not get channel info: {e}")
        return ""

async def get_group_admins(client, entity):
    """Get admins from a group"""
    try:
        participants = client.iter_participants(entity, filter=ChannelParticipantsAdmins)
        admins = []
        async for participant in participants:
            if participant.username:
                admins.append(f"@{participant.username}")
            else:
                admins.append(participant.first_name or "Unknown")
        return admins
    except Exception as e:
        print(f"  Could not fetch admins: {e}")
        return []

async def scan_pinned_messages(client, entity):
    """Scan pinned messages for admin information"""
    try:
        pinned_messages = await client.get_messages(entity, ids=[])
        contacts = []
        for msg in pinned_messages:
            if msg and msg.text:
                print(f"Pinned message: {msg.text[:100]}...")
                msg_contacts = extract_contacts_from_text(msg.text)
                contacts.extend(msg_contacts)
        return list(set(contacts))
    except Exception as e:
        print(f"Could not get pinned messages: {e}")
        return []

async def scan_messages_for_contacts(client, entity, limit=100):
    """Scan messages for contact information"""
    try:
        admin_mentions = []
        async for message in client.iter_messages(entity, limit=limit):
            if message and message.text:
                # Look for admin mentions
                admin_patterns = [
                    r'@(\w+)',  # Usernames
                    r'admin[:\s]+@(\w+)',  # Admin: @username
                    r'owner[:\s]+@(\w+)',  # Owner: @username
                    r'contact[:\s]+@(\w+)',  # Contact: @username
                    r'https://t\.me/(\w+)',  # t.me links
                ]
                
                for pattern in admin_patterns:
                    matches = re.findall(pattern, message.text, re.IGNORECASE)
                    admin_mentions.extend(matches)
        
        return [f"@{mention}" for mention in set(admin_mentions)]
    except Exception as e:
        print(f"Could not scan messages: {e}")
        return []

async def join_and_analyze_community_group(client, group_username):
    """Join a community group and analyze its admins"""
    try:
        print(f"  🔍 Analyzing community group: {group_username}")
        
        # Try to join the group
        try:
            await client(JoinChannelRequest(channel=group_username))
            print(f"  ✅ Joined group: {group_username}")
            
            # Get group entity
            group_entity = await client.get_entity(group_username)
            
            # Get admins
            admins = await get_group_admins(client, group_entity)
            if admins:
                print(f"  ✅ Group admins found: {admins}")
            
            # Check group description
            try:
                full_group = await client(functions.channels.GetFullChannelRequest(channel=group_entity))
                if full_group.full_chat.about:
                    print(f"  Group description: {full_group.full_chat.about}")
                    desc_contacts = extract_contacts_from_text(full_group.full_chat.about)
                    if desc_contacts:
                        print(f"  ✅ Contacts in group description: {desc_contacts}")
                        admins.extend(desc_contacts)
            except Exception as e:
                print(f"  Could not get group description: {e}")
            
            return admins
            
        except Exception as e:
            print(f"  Could not join group {group_username}: {e}")
            return []
            
    except Exception as e:
        print(f"  Error analyzing group {group_username}: {e}")
        return []

async def enhanced_channel_analysis(client, username):
    """Enhanced channel analysis using multiple methods"""
    print(f"\n{'='*50}")
    print(f"Processing channel: {username}")
    print(f"{'='*50}")
    
    all_contacts = []
    community_links = []
    
    try:
        entity = await client.get_entity(username)
        
        # Method 1: Get channel description
        description = await get_channel_info(client, username)
        if description:
            desc_contacts = extract_contacts_from_text(description)
            if desc_contacts:
                print(f"Contacts found in description: {desc_contacts}")
                all_contacts.extend(desc_contacts)
        
        # Method 2: Scan pinned messages
        print("\n📌 Scanning pinned messages...")
        pinned_contacts = await scan_pinned_messages(client, entity)
        if pinned_contacts:
            print(f"✅ Contacts found in pinned messages: {pinned_contacts}")
            all_contacts.extend(pinned_contacts)
        
        # Method 3: Scan recent messages for contacts
        print("\n📱 Scanning recent messages for contacts...")
        message_contacts = await scan_messages_for_contacts(client, entity, limit=50)
        if message_contacts:
            print(f"✅ Contacts found in messages: {message_contacts}")
            all_contacts.extend(message_contacts)
        
        # Method 4: Try to get admins directly (usually fails for broadcast channels)
        print("\nTrying to get admins from channel...")
        try:
            admins = await get_group_admins(client, entity)
            if admins:
                print(f"✅ Direct admins found: {admins}")
                all_contacts.extend(admins)
        except Exception as e:
            print(f"  Could not fetch admins: {e}")
        
        # Method 5: Scan for community groups and join them
        if not all_contacts:
            print(f"\n❌ No contacts found for {username}")
            print("Scanning all posts in {username} for group/community links...")
            
            group_keywords = ['chat', 'group', 'community', 'discussion', 'support', 'help']
            found_group_links = set()
            
            async for message in client.iter_messages(entity, limit=None):
                if message and message.text:
                    # Find t.me links
                    tme_links = re.findall(r'https://t\.me/(\w+)', message.text)
                    for link in tme_links:
                        # Check if link contains group-related keywords
                        if any(keyword in link.lower() for keyword in group_keywords):
                            found_group_links.add(link)
                    
                    # Also look for @mentions that might be groups
                    mentions = re.findall(r'@(\w+)', message.text)
                    for mention in mentions:
                        if any(keyword in mention.lower() for keyword in group_keywords):
                            found_group_links.add(mention)
            
            if found_group_links:
                print(f"Found group/community links in posts: {list(found_group_links)}")
                
                # Filter links to only include those similar to the channel name
                filtered_group_links = [
                    link for link in found_group_links
                    if username.lower() in link.lower()
                ]
                
                if filtered_group_links:
                    print(f"Filtered group links: {filtered_group_links}")
                    
                    # Try to join and analyze community groups
                    for group_link in filtered_group_links[:3]:  # Limit to first 3
                        group_admins = await join_and_analyze_community_group(client, group_link)
                        if group_admins:
                            all_contacts.extend(group_admins)
                            community_links.append(f"https://t.me/{group_link}")
                
                # If no filtered links, try some of the found links
                elif found_group_links:
                    print(f"Trying unfiltered group links: {list(found_group_links)[:2]}")
                    for group_link in list(found_group_links)[:2]:
                        group_admins = await join_and_analyze_community_group(client, group_link)
                        if group_admins:
                            all_contacts.extend(group_admins)
                            community_links.append(f"https://t.me/{group_link}")
        
        # Remove duplicates and format results
        unique_contacts = list(set(all_contacts))
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
        
    except Exception as e:
        print(f"❌ Error processing {username}: {e}")
        return {
            'channel': username,
            'contacts': [],
            'community_links': []
        }

async def main():
    """Main function"""
    client = TelegramClient(session_name, api_id, api_hash)
    
    try:
        await client.start()
        print("✅ Successfully connected to Telegram!")
        
        # Read channels
        channels = read_channel_usernames()
        print(f"📋 Found {len(channels)} channels to process")
        
        # Process results
        results = []
        
        for i, username in enumerate(channels, 1):
            print(f"\n🔄 Processing {i}/{len(channels)}: {username}")
            
            # Add delay to avoid rate limits
            if i > 1:
                delay = random.uniform(2, 5)
                print(f"⏳ Waiting {delay:.1f} seconds...")
                await asyncio.sleep(delay)
            
            result = await enhanced_channel_analysis(client, username)
            results.append(result)
        
        # Export results to CSV
        print(f"\n📊 Exporting results to CSV...")
        with open('enhanced_channel_results.csv', 'w', newline='', encoding='utf-8') as csvfile:
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
        
        print("✅ Results exported to enhanced_channel_results.csv")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main()) 