import gspread
from google.oauth2.service_account import Credentials

# Google Sheets setup
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    'service_account.json', scopes=SCOPES
)

gc = gspread.authorize(credentials)
spreadsheet_id = '19IuLIlAOlzoiiqY4S55tG8PHkzupPauvCGfX0VvcfK0'
sheet = gc.open_by_key(spreadsheet_id).sheet1

# Read all data from the sheet
all_data = sheet.get_all_values()

print("=== CHECKING FOR NEW CHANNELS (ROW 64+) ===")
new_channels = []
for i, row in enumerate(all_data[63:], 64):  # Start from row 64 (index 63)
    if row and len(row) > 0 and row[0]:  # If column A has data
        print(f"Row {i}: {row[0]}")
        # Extract channel name from URL
        if 'https://t.me/' in row[0]:
            channel_name = row[0].replace('https://t.me/', '')
        else:
            channel_name = row[0]
        new_channels.append(channel_name)

if new_channels:
    print(f"\nTotal new channels found: {len(new_channels)}")
    print("New channels list:", new_channels)
    
    # Update channels.txt with new channels
    with open('channels.txt', 'r') as f:
        existing_channels = [line.strip() for line in f if line.strip()]
    
    # Add new channels that aren't already in the file
    channels_to_add = []
    for channel in new_channels:
        if channel not in existing_channels:
            channels_to_add.append(channel)
    
    if channels_to_add:
        print(f"\nAdding {len(channels_to_add)} new channels to channels.txt")
        with open('channels.txt', 'a') as f:
            for channel in channels_to_add:
                f.write(f"\n{channel}")
        print("✅ Updated channels.txt")
    else:
        print("✅ All channels already in channels.txt")
else:
    print("No new channels found from row 64 onward") 