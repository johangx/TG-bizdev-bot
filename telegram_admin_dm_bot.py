import asyncio
import time
import random
import re
import csv
from telethon import TelegramClient
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.errors import FloodWaitError, PeerFloodError, UserPrivacyRestrictedError
from telethon.tl import functions

# === CONFIGURATION ===
api_id = 24967410  # Your Telegram API ID
api_hash = 'a772e39631b4b245de2b0fafd1850a71'  # Your Telegram API Hash
session_name = 'admin_dm_session'  # Session file name
channels_file = 'channels.txt'  # File with channel usernames (one per line)
message_templates = [
    "Hello {}, I found your channel and wanted to reach out...",
    "Hi {}, hope you're doing well. I wanted to connect about your channel.",
    "Hey {}! I have a question about your channel."
]

# === MAIN SCRIPT ===
def read_channel_usernames(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

def personalize_message(admin, templates):
    name = admin.first_name or admin.username or "there"
    return random.choice(templates).format(name)

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
        
        # Get linked discussion group if exists
        linked_chat = None
        try:
            if hasattr(full_chat.full_chat, 'linked_chat') and full_chat.full_chat.linked_chat:
                linked_chat = full_chat.full_chat.linked_chat
        except:
            pass
        
        return entity, about, linked_chat
    except Exception as e:
        print(f"  Could not access {username}: {e}")
        return None, "", None

async def get_group_admins(client, entity):
    """Get admins from a group/supergroup"""
    try:
        admins = []
        async for admin in client.iter_participants(entity, filter=ChannelParticipantsAdmins):
            if not getattr(admin, 'bot', False) and not getattr(admin, 'is_self', False):
                admins.append(admin)
        return admins
    except Exception as e:
        print(f"  Could not fetch admins: {e}")
        return []

async def main():
    client = TelegramClient(session_name, api_id, api_hash)
    await client.start(phone=lambda: input("Enter your phone number: "))

    channel_usernames = read_channel_usernames(channels_file)
    results = []  # For CSV export
    
    for username in channel_usernames:
        print(f"\n{'='*50}")
        print(f"Processing channel: {username}")
        print(f"{'='*50}")
        broadcast_link = f"https://t.me/{username}"
        community_links = []
        admin_list = []
        
        # Get channel info
        entity, about, linked_chat = await get_channel_info(client, username)
        if not entity:
            continue
        
        print(f"Channel: {entity.title}")
        if about:
            print(f"Description: {about[:200]}...")
        
        # Method 1: Extract contacts from description
        contacts_from_desc = extract_contacts_from_text(about)
        if contacts_from_desc:
            print(f"Contacts found in description: {contacts_from_desc}")
            admin_list.extend(contacts_from_desc)
        
        # Method 2: Try to get admins from the channel itself (if you're admin)
        print("\nTrying to get admins from channel...")
        channel_admins = await get_group_admins(client, entity)
        if channel_admins:
            print(f"Channel admins found: {len(channel_admins)}")
            for admin in channel_admins:
                print(f"  - {admin.username or admin.first_name or admin.id}")
                if admin.username:
                    admin_list.append(f"@{admin.username}")
        
        # Method 3: Try linked discussion group
        discussion_admins = []
        if linked_chat:
            print(f"\nFound linked discussion group: {linked_chat.title}")
            print("Trying to get admins from discussion group...")
            discussion_admins = await get_group_admins(client, linked_chat)
            if discussion_admins:
                print(f"Discussion group admins found: {len(discussion_admins)}")
                for admin in discussion_admins:
                    print(f"  - {admin.username or admin.first_name or admin.id}")
                    if admin.username:
                        admin_list.append(f"@{admin.username}")
            # Add linked chat link
            if hasattr(linked_chat, 'username') and linked_chat.username:
                community_links.append(f"https://t.me/{linked_chat.username}")
        
        all_contacts = contacts_from_desc + [f"@{admin.username}" for admin in channel_admins + discussion_admins if admin.username]
        if all_contacts:
            print(f"\n✅ Total contacts found: {len(set(all_contacts))}")
            print(f"Contacts: {list(set(all_contacts))}")
        else:
            print(f"\n❌ No contacts found for {username}")
            # Scan all posts for group/community links if no contact found
            print(f"Scanning all posts in {username} for group/community links...")
            group_keywords = [
                'join our group', 'community', 'discussion', 'chat', 'join group', 'join us', 'group link', 'discussion group', 'community group', 'join the group', 'join the chat', 'join our community'
            ]
            found_group_links = set()
            try:
                async for message in client.iter_messages(entity, limit=None):
                    text = (message.text or "").lower()
                    # Look for group keywords
                    if any(keyword in text for keyword in group_keywords):
                        links = re.findall(r"https://t\.me/[\w_]+", message.text or "")
                        for link in links:
                            if link != f"https://t.me/{username}":
                                found_group_links.add(link)
                    # Also add any t.me links that are not the channel itself
                    links = re.findall(r"https://t\.me/[\w_]+", message.text or "")
                    for link in links:
                        if link != f"https://t.me/{username}":
                            found_group_links.add(link)
                if found_group_links:
                    # Only keep links where the group username contains the broadcast channel's name
                    filtered_group_links = [
                        link for link in found_group_links
                        if username.lower() in link.lower()
                    ]
                    print(f"Found group/community links in posts: {filtered_group_links}")
                    for link in filtered_group_links:
                        community_links.append(link)
                        group_username = link.split("https://t.me/")[-1]
                        try:
                            group_entity = await client.get_entity(group_username)
                        except Exception as e:
                            print(f"    Could not get group entity for {group_username}: {e}")
                            continue
                        print(f"    Fetching admins for group: {group_username}")
                        group_admins = await get_group_admins(client, group_entity)
                        if group_admins:
                            print(f"    Group admins found: {len(group_admins)}")
                            for admin in group_admins:
                                print(f"      - {admin.username or admin.first_name or admin.id}")
                                if admin.username:
                                    admin_list.append(f"@{admin.username}")
                        else:
                            print(f"    No admins found for group: {group_username}")
                else:
                    print("No group/community links found in posts.")
            except Exception as e:
                print(f"  Could not scan all posts: {e}")
        # Save result for CSV
        results.append([
            broadcast_link,
            ", ".join(community_links) if community_links else "",
            ", ".join(sorted(set(admin_list))) if admin_list else ""
        ])
        print(f"{'='*50}")

    # Export to CSV
    with open("channel_admins_results.csv", "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Broadcast Channel Link", "Community Chat Links", "Admins (comma-separated)"])
        writer.writerows(results)
    print("\nResults exported to channel_admins_results.csv\n")

    # Send message to specific admin
    print("\nSending message to @photofixer...")
    try:
        await client.send_message("@photofixer", "GM")
        print("✅ Message sent successfully to @photofixer")
    except Exception as e:
        print(f"❌ Could not send message to @photofixer: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 