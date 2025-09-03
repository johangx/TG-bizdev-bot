import asyncio
import re
import time
from telethon import TelegramClient, functions
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import ChannelParticipantsAdmins

# === CONFIGURATION ===
api_id = 24967410
api_hash = 'a772e39631b4b245de2b0fafd1850a71'
session_name = 'admin_dm_session'

async def detect_group_owner_advanced():
    client = TelegramClient(session_name, api_id, api_hash)
    
    try:
        await client.start()
        print("✅ Connected to Telegram!")
        
        # Test with a known channel
        test_channel = "https://t.me/toncoin"
        
        print(f"\n🔍 Analyzing: {test_channel}")
        
        # Method 1: Get channel entity
        try:
            entity = await client.get_entity(test_channel)
            print(f"Channel: {entity.title}")
            
            # Method 2: Try to get full channel info
            try:
                full_channel = await client(functions.channels.GetFullChannelRequest(channel=entity))
                print(f"Description: {full_channel.full_chat.about}")
                
                # Extract contacts from description
                contacts = extract_contacts_from_text(full_channel.full_chat.about)
                if contacts:
                    print(f"✅ Contacts found in description: {contacts}")
                
            except Exception as e:
                print(f"Could not get full channel info: {e}")
            
            # Method 3: Scan recent messages for admin info
            print("\n📱 Scanning recent messages for admin info...")
            admin_mentions = []
            async for message in client.iter_messages(entity, limit=50):
                if message.text:
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
            
            if admin_mentions:
                print(f"✅ Admin mentions found in messages: {list(set(admin_mentions))}")
            
            # Method 4: Look for pinned messages
            print("\n📌 Checking pinned messages...")
            try:
                pinned_messages = await client.get_messages(entity, ids=[])
                if pinned_messages:
                    for msg in pinned_messages:
                        if msg.text:
                            print(f"Pinned message: {msg.text[:100]}...")
                            contacts = extract_contacts_from_text(msg.text)
                            if contacts:
                                print(f"✅ Contacts in pinned message: {contacts}")
            except Exception as e:
                print(f"Could not get pinned messages: {e}")
            
            # Method 5: Try to join community groups and analyze
            print("\n👥 Looking for community groups...")
            community_groups = []
            async for message in client.iter_messages(entity, limit=100):
                if message.text:
                    # Find group links
                    group_links = re.findall(r'https://t\.me/(\w+)', message.text)
                    for link in group_links:
                        if 'chat' in link.lower() or 'group' in link.lower() or 'community' in link.lower():
                            community_groups.append(link)
            
            if community_groups:
                print(f"✅ Community groups found: {community_groups[:3]}")  # Limit to first 3
                
                # Try to join and analyze one group
                for group in community_groups[:1]:  # Just try the first one
                    try:
                        print(f"\n🔍 Analyzing community group: {group}")
                        
                        # Try to join the group
                        try:
                            await client(JoinChannelRequest(channel=group))
                            print(f"✅ Joined group: {group}")
                            
                            # Get group entity
                            group_entity = await client.get_entity(group)
                            
                            # Try to get admins
                            try:
                                participants = client.iter_participants(group_entity, filter=ChannelParticipantsAdmins)
                                admins = []
                                async for participant in participants:
                                    if participant.username:
                                        admins.append(f"@{participant.username}")
                                    else:
                                        admins.append(participant.first_name or "Unknown")
                                
                                if admins:
                                    print(f"✅ Group admins found: {admins}")
                                
                            except Exception as e:
                                print(f"Could not get admins: {e}")
                            
                            # Check group description
                            try:
                                full_group = await client(functions.channels.GetFullChannelRequest(channel=group_entity))
                                if full_group.full_chat.about:
                                    print(f"Group description: {full_group.full_chat.about}")
                                    contacts = extract_contacts_from_text(full_group.full_chat.about)
                                    if contacts:
                                        print(f"✅ Contacts in group description: {contacts}")
                            except Exception as e:
                                print(f"Could not get group description: {e}")
                            
                        except Exception as e:
                            print(f"Could not join group {group}: {e}")
                            
                    except Exception as e:
                        print(f"Error analyzing group {group}: {e}")
            
        except Exception as e:
            print(f"Error analyzing channel: {e}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await client.disconnect()

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

if __name__ == "__main__":
    asyncio.run(detect_group_owner_advanced()) 