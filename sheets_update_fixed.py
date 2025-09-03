import gspread
from google.oauth2.service_account import Credentials

# Service account file and spreadsheet ID
SERVICE_ACCOUNT_FILE = 'service_account.json'
SPREADSHEET_ID = '19IuLIlAOlzoiiqY4S55tG8PHkzupPauvCGfX0VvcfK0'

# CORRECT MAPPING BASED ON ACTUAL CHANNEL NAMES IN THE SHEET
updates = [
    {'row': 2, 'channel': 'anime', 'admin': '@strategy', 'community': 'N/A'},
    {'row': 3, 'channel': 'insta', 'admin': '@strategy', 'community': 'N/A'},
    {'row': 4, 'channel': 'spotify', 'admin': '@strategy', 'community': 'N/A'},
    {'row': 5, 'channel': 'netflix', 'admin': '@strategy', 'community': 'N/A'},
    {'row': 6, 'channel': 'NeuralZone', 'admin': '@NeuralZone, @photofixer', 'community': 'N/A'},
    {'row': 7, 'channel': 'stukach_trading', 'admin': '@TGowner999', 'community': 'N/A'},
    {'row': 8, 'channel': 'Kripto_Azbuk', 'admin': '@TGowner999', 'community': 'N/A'},
    {'row': 9, 'channel': 'finansist_busines', 'admin': '@TGowner999', 'community': 'N/A'},
    {'row': 10, 'channel': 'INSIDERR_POLITIC', 'admin': '@TGowner999, @topovik_999', 'community': 'N/A'},
    {'row': 11, 'channel': 'Sport_HUB_football', 'admin': '@TGowner999, @topovik_999', 'community': 'N/A'},
    {'row': 12, 'channel': 'tonkingsquad', 'admin': '@tonkingram, @tonmoneybag', 'community': 'N/A'},
    {'row': 13, 'channel': 'obeie', 'admin': '@Sa4iz1k, @gargoniel, @killhpx, @kykysik00, @ostapsmm, @pifagor_dao, @sa4iz1k, @tocatcrypto, @twall_ads, @vladuah', 'community': 'N/A'},
    {'row': 14, 'channel': 'CryptoDvisj', 'admin': '@Arch1k3, @Boomerbae, @Imijj0, @MemoryOfLegendary, @Sa4iz1k, @SheikhOfficiaI, @egor_unique, @exmanager_crypto, @nikolacoach, @tocatcrypto, @vofi555, @woskish', 'community': 'N/A'},
    {'row': 15, 'channel': 'backdoordegens', 'admin': '@llutfullah', 'community': 'N/A'},
    {'row': 16, 'channel': 'TONContentEnglish', 'admin': '@ad_crypto', 'community': 'N/A'},
    {'row': 17, 'channel': 'garden_btc', 'admin': '@ad_crypto', 'community': 'N/A'},
    {'row': 18, 'channel': 'W3BFLIX', 'admin': '@Crypto_Techware2, @Ghost4Bridge, @Makavelllly, @MamaPips, @MockinBirds, @Ovroahmed2, @anurakyaser, @mennick', 'community': 'https://t.me/W3BFLIXBot__\nhttps://t.me/W3BFLIXBot\nhttps://t.me/W3BFLIX_Group__\nhttps://t.me/W3BFLIX_Group'},
    {'row': 19, 'channel': 'tonologiaENG', 'admin': '@Sonnov_official, @sonnov_official', 'community': 'N/A'},
    {'row': 20, 'channel': 'thetonstakers', 'admin': '@tonstakers_support_bot', 'community': 'N/A'},
    {'row': 21, 'channel': 'GemHunterrs', 'admin': '@MEXCEnglish, @TonyStvrk, @bitcoinV2Channel, @bmxcommunity', 'community': 'N/A'},
    {'row': 22, 'channel': 'OnTopTM', 'admin': '@AnoMessBot, @DevMti, @HowAllBot, @OnTopAds, @OnTopSupport, @ontopads', 'community': 'N/A'},
    {'row': 23, 'channel': 'cryptosayer', 'admin': 'https://t.me/kryptoadv', 'community': 'N/A'}
]

print("Starting Google Sheets update with CORRECT channel mapping...")

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
    
    # Update the data using the correct format
    for update in updates:
        try:
            # Update column B (Admin) - using cell reference
            if update['admin']:
                sheet.update_cell(update['row'], 2, update['admin'])  # row, column number
                print(f"✅ Row {update['row']} ({update['channel']}) Column B updated: {update['admin']}")
            else:
                sheet.update_cell(update['row'], 2, '')  # Empty cell for no admin
                print(f"✅ Row {update['row']} ({update['channel']}) Column B updated: (empty)")
            
            # Update column C (Community) - using cell reference with line breaks
            sheet.update_cell(update['row'], 3, update['community'])  # row, column number
            print(f"✅ Row {update['row']} ({update['channel']}) Column C updated: {update['community']}")
            
        except Exception as e:
            print(f"❌ Error updating row {update['row']}: {e}")
    
    print("\n✅ Google Sheets update completed successfully!")
    print(f"Updated {len(updates)} rows with admin and community data.")

except FileNotFoundError:
    print(f"❌ Service account file '{SERVICE_ACCOUNT_FILE}' not found!")
    print("Please make sure the service_account.json file is in the current directory.")
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nThe service account authentication failed. Please check:")
    print("1. The service_account.json file is in the current directory")
    print("2. The service account has permission to access the Google Sheet")
    print("3. The Google Sheet ID is correct") 