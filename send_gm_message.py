import asyncio
from telethon import TelegramClient

# === CONFIGURATION ===
api_id = 24967410
api_hash = 'a772e39631b4b245de2b0fafd1850a71'
session_name = 'admin_dm_session'

# Message to send
message = "GM"

# Target user
target_user = "@Bridgetplayer1"

async def send_gm_message():
    client = TelegramClient(session_name, api_id, api_hash)
    
    try:
        await client.start()
        print("✅ Successfully connected to Telegram!")
        
        # Send the message
        try:
            result = await client.send_message(target_user, message)
            print(f"✅ Message sent successfully!")
            print(f"Message ID: {result.id}")
            print(f"Sent to: {target_user}")
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(send_gm_message()) 