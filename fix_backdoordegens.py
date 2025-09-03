import gspread
from google.oauth2.service_account import Credentials

# Service account file and spreadsheet ID
SERVICE_ACCOUNT_FILE = 'service_account.json'
SPREADSHEET_ID = '19IuLIlAOlzoiiqY4S55tG8PHkzupPauvCGfX0VvcfK0'

# CORRECT backdoordegens admin data based on the channel info
fixes = [
    {'row': 15, 'channel': 'backdoordegens', 'admin': '@woskish, @MemoryOfLegendary, @vofi555, @Boomerbae', 'community': 'N/A'},  # Fix: correct owners and managers
]

print("Fixing backdoordegens admin data...")

try:
    # Define the scope for Google Sheets API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    
    # Authenticate using the service account JSON file
    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scope)
    gc = gspread.authorize(credentials)
    
    print("✅ Successfully authenticated with service account!")
    
    # Open the spreadsheet
    sheet = gc.open_by_key(SPREADSHEET_ID).sheet1
    
    print("✅ Successfully connected to Google Sheets!")
    
    # Fix the backdoordegens admin data
    for fix in fixes:
        try:
            # Update column B (Admin)
            sheet.update_cell(fix['row'], 2, fix['admin'])
            print(f"✅ Row {fix['row']} ({fix['channel']}) Column B FIXED: {fix['admin']}")
            
            # Update column C (Community)
            sheet.update_cell(fix['row'], 3, fix['community'])
            print(f"✅ Row {fix['row']} ({fix['channel']}) Column C updated: {fix['community']}")
            
        except Exception as e:
            print(f"❌ Error fixing row {fix['row']}: {e}")
    
    print("\n✅ backdoordegens admin data fixed!")

except FileNotFoundError:
    print(f"❌ Service account file '{SERVICE_ACCOUNT_FILE}' not found!")
except Exception as e:
    print(f"❌ Error: {e}") 