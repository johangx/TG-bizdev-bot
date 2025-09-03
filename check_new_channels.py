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

print("=== ALL CHANNELS IN SHEET ===")
for i, row in enumerate(all_data, 1):
    if row[0]:  # If column A has data
        print(f"Row {i}: {row[0]}")

print("\n=== NEW CHANNELS (ROW 24+) ===")
new_channels = []
for i, row in enumerate(all_data[23:], 24):  # Start from row 24 (index 23)
    if row[0]:  # If column A has data
        print(f"Row {i}: {row[0]}")
        new_channels.append(row[0])

print(f"\nTotal new channels found: {len(new_channels)}")
print("New channels list:", new_channels) 