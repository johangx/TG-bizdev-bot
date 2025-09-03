import gspread
import time
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

# Remaining rows that hit rate limits
remaining_updates = [
    {'row': 57, 'admin': '@catsdogs_game_bot', 'community': 'N/A'},
    {'row': 58, 'admin': '@FintopioNews, @fintopio', 'community': 'N/A'},
    {'row': 59, 'admin': '@bill_bdbz, @buzzit1_bot, @sandy_support', 'community': 'N/A'},
    {'row': 60, 'admin': '@rocky_rabbit_bot', 'community': 'N/A'},
    {'row': 61, 'admin': 'N/A', 'community': 'N/A'},
    {'row': 62, 'admin': 'N/A', 'community': 'N/A'},
    {'row': 63, 'admin': 'N/A', 'community': 'N/A'}
]

print("Updating remaining rows (57-63) that hit rate limits...")

for update in remaining_updates:
    try:
        # Update admin column (B)
        sheet.update_cell(update['row'], 2, update['admin'])
        print(f"✅ Row {update['row']} - Admin: {update['admin']}")
        
        # Update community column (C)
        sheet.update_cell(update['row'], 3, update['community'])
        print(f"✅ Row {update['row']} - Community: {update['community']}")
        
        # Add delay between updates to avoid rate limits
        time.sleep(1)
        
    except Exception as e:
        print(f"❌ Error updating row {update['row']}: {e}")

print("\n🎯 **Remaining Rows Update Complete!**")
print(f"✅ Updated {len(remaining_updates)} remaining rows (57-63)") 