import asyncio
from telethon import TelegramClient

# === CONFIGURATION ===
api_id = 24967410
api_hash = 'a772e39631b4b245de2b0fafd1850a71'
session_name = 'admin_dm_session'

# Message to send
message = """GM! 👋

I'm Johan from the GOAT Gaming team. We noticed you haven't been back in the app lately and would love to hear your thoughts.

We're rolling out fresh updates, and your feedback will help us make the game even more fun to return to.

👉 Share your thoughts here: https://forms.gle/34hY4zrKbvscWqcP8

🎁 You'll get 100K Pepe Points + 100 Raffle Tickets as a thank you.

Thanks for being part of the community — we're listening 💛"""

# List of users to message
users_to_message = [
    "@Benahmad2",
    "@BuscoONE",
    "@maryno4ka22",
    "@mdsweethossain",
    "@Hashemi1969",
    "@MongBak",
    "@nurmuhammadjonim224",
    "@Vuson280999",
    "@andyjamyy",
    "@Brat_bruhi1z"
]

async def send_messages():
    """Send the message to all specified users"""
    client = TelegramClient(session_name, api_id, api_hash)
    
    try:
        await client.start()
        print("✅ Successfully connected to Telegram!")
        
        for i, user in enumerate(users_to_message, 1):
            try:
                print(f"\n🔄 Sending message {i}/{len(users_to_message)} to {user}...")
                
                # Send the message
                await client.send_message(user, message)
                print(f"✅ Message sent successfully to {user}")
                
                # Add delay to avoid rate limits
                if i < len(users_to_message):
                    delay = 3  # 3 seconds between messages
                    print(f"⏳ Waiting {delay} seconds...")
                    await asyncio.sleep(delay)
                    
            except Exception as e:
                print(f"❌ Failed to send message to {user}: {e}")
                continue
        
        print(f"\n🎯 **Message Sending Complete!**")
        print(f"✅ Attempted to send messages to {len(users_to_message)} users")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(send_messages())
