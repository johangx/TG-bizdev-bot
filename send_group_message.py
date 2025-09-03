import asyncio
from telethon import TelegramClient
from telethon.tl.functions.messages import ImportChatInviteRequest

# === CONFIGURATION ===
api_id = 24967410
api_hash = 'a772e39631b4b245de2b0fafd1850a71'
session_name = 'admin_dm_session'

# Message to send
message = "not the best ROI, but that's kind of what we expected since high views don't always mean high CTR. Still really appreciate the push on your side tho"

# Group link
group_link = "https://t.me/+Ha0ehflYqvMxMDBh"

async def send_message_to_group():
    client = TelegramClient(session_name, api_id, api_hash)
    
    try:
        await client.start()
        print("✅ Successfully connected to Telegram!")
        
        # Extract the invite hash from the link
        invite_hash = group_link.split('/')[-1]
        print(f"Invite hash: {invite_hash}")
        
        # Join the group first (if not already a member)
        try:
            await client(ImportChatInviteRequest(hash=invite_hash))
            print("✅ Joined the group successfully!")
        except Exception as e:
            print(f"Note: {e} (might already be a member)")
        
        # Send the message
        try:
            result = await client.send_message(group_link, message)
            print(f"✅ Message sent successfully!")
            print(f"Message ID: {result.id}")
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(send_message_to_group()) 