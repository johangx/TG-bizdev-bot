import gspread
from google.oauth2.service_account import Credentials

# Service account file and spreadsheet ID
SERVICE_ACCOUNT_FILE = 'service_account.json'
SPREADSHEET_ID = '19IuLIlAOlzoiiqY4S55tG8PHkzupPauvCGfX0VvcfK0'

print("Reading actual Google Sheet data...")

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
    
    # Read the actual data from the sheet
    print("\n=== ACTUAL SHEET DATA ===")
    print("Row | Channel | Admin | Community")
    print("----|---------|-------|----------")
    
    for row in range(2, 25):  # Rows 2-24
        try:
            channel = sheet.cell(row, 1).value  # Column A
            admin = sheet.cell(row, 2).value    # Column B
            community = sheet.cell(row, 3).value # Column C
            
            if channel:  # Only show rows with channels
                print(f"{row:3} | {channel:20} | {admin:30} | {community}")
            else:
                print(f"{row:3} | (empty)               | {admin:30} | {community}")
                
        except Exception as e:
            print(f"{row:3} | Error reading row: {e}")
    
    print("\n=== END OF SHEET DATA ===")

except FileNotFoundError:
    print(f"❌ Service account file '{SERVICE_ACCOUNT_FILE}' not found!")
except Exception as e:
    print(f"❌ Error: {e}") 