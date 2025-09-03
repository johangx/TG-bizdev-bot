import asyncio
import re
from telethon import TelegramClient
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.tl import functions

# === CONFIGURATION ===
api_id = 24967410
api_hash = 'a772e39631b4b245de2b0fafd1850a71'
session_name = 'admin_dm_session'

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
    
    # Scan recent messages for contacts and group links
    print("\nScanning recent messages for contacts and group links...")
    try:
        message_count = 0
        max_messages = 20  # Scan last 20 messages
        
        async for message in client.iter_messages(entity, limit=max_messages):
            message_count += 1
            if message.text:
                print(f"\n--- Message {message_count} ---")
                print(f"Text: {message.text[:200]}...")  # Show first 200 chars
                
                # Extract contacts from message text
                message_contacts = extract_contacts_from_text(message.text)
                if message_contacts:
                    print(f"Contacts found: {message_contacts}")
                    contacts.extend(message_contacts)
                
                # Look for t.me links (potential group links)
                t_me_links = re.findall(r'https://t\.me/(\w+)', message.text)
                if t_me_links:
                    print(f"🔗 t.me links found: {t_me_links}")
                    # Add as potential group links
                    for link in t_me_links:
                        contacts.append(f"https://t.me/{link}")
                
                # Look for invite links
                invite_links = re.findall(r'https://t\.me/\+(\w+)', message.text)
                if invite_links:
                    print(f"🔗 Invite links found: {invite_links}")
                    for link in invite_links:
                        contacts.append(f"https://t.me/+{link}")
                
                # Look for community indicators
                community_keywords = ['community', 'group', 'chat', 'discussion', 'network', 'forum']
                if any(keyword in message.text.lower() for keyword in community_keywords):
                    print(f"💬 Community-related content detected!")
                    
                # Look for @mentions (potential community handles)
                mentions = re.findall(r'@(\w+)', message.text)
                if mentions:
                    print(f"👥 Mentions found: {mentions}")
                    for mention in mentions:
                        contacts.append(f"@{mention}")
                
                if message_count >= max_messages:
                    break
                    
    except Exception as e:
        print(f"  Could not scan messages: {e}")
    
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
        
        # Scan the yoo_stars channel
        result = await scan_channel_for_admins(client, "yoo_stars")
        
        print(f"\n🎯 **Scan Complete!**")
        print(f"Channel: {result['channel']}")
        print(f"Admin/Contact Info: {result['contacts']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
