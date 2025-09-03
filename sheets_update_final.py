import gspread
from google.oauth2.service_account import Credentials

# Service account file and spreadsheet ID
SERVICE_ACCOUNT_FILE = 'service_account.json'
SPREADSHEET_ID = '19IuLIlAOlzoiiqY4S55tG8PHkzupPauvCGfX0VvcfK0'

# Data to update (from the CSV results) - CORRECTED MAPPING
updates = [
    {'row': 2, 'admin': '@strategy', 'community': 'N/A'},  # anime
    {'row': 3, 'admin': '@strategy', 'community': 'N/A'},  # insta
    {'row': 4, 'admin': '@strategy', 'community': 'N/A'},  # spotify
    {'row': 5, 'admin': '@strategy', 'community': 'N/A'},  # netflix
    {'row': 6, 'admin': '@NeuralZone, @photofixer', 'community': 'N/A'},  # NeuralZone
    {'row': 7, 'admin': '@TGowner999', 'community': 'N/A'},  # stukach_trading
    {'row': 8, 'admin': '@TGowner999', 'community': 'N/A'},  # Kripto_Azbuk
    {'row': 9, 'admin': '@TGowner999', 'community': 'N/A'},  # finansist_busines
    {'row': 10, 'admin': '@TGowner999, @topovik_999', 'community': 'N/A'},  # INSIDERR_POLITIC
    {'row': 11, 'admin': '@TGowner999, @topovik_999', 'community': 'N/A'},  # Sport_HUB_football
    {'row': 12, 'admin': '@tonkingram, @tonmoneybag', 'community': 'N/A'},  # tonkingsquad
    {'row': 13, 'admin': '@Sa4iz1k, @gargoniel, @killhpx, @kykysik00, @ostapsmm, @pifagor_dao, @sa4iz1k, @tocatcrypto, @twall_ads, @vladuah', 'community': 'N/A'},  # CryptoDvisj
    {'row': 14, 'admin': '@Arch1k3, @Boomerbae, @Imijj0, @MemoryOfLegendary, @Sa4iz1k, @SheikhOfficiaI, @egor_unique, @exmanager_crypto, @nikolacoach, @tocatcrypto, @vofi555, @woskish', 'community': 'N/A'},  # backdoordegens
    {'row': 15, 'admin': '@llutfullah', 'community': 'N/A'},  # TONContentEnglish
    {'row': 16, 'admin': '@ad_crypto', 'community': 'N/A'},  # garden_btc
    {'row': 17, 'admin': '@Crypto_Techware2, @Ghost4Bridge, @Makavelllly, @MamaPips, @MockinBirds, @Ovroahmed2, @anurakyaser, @mennick', 'community': 'https://t.me/W3BFLIXBot__\nhttps://t.me/W3BFLIXBot\nhttps://t.me/W3BFLIX_Group__\nhttps://t.me/W3BFLIX_Group'},  # W3BFLIX
    {'row': 18, 'admin': '@Sonnov_official, @sonnov_official', 'community': 'N/A'},  # tonologiaENG
    {'row': 19, 'admin': '@tonstakers_support_bot', 'community': 'N/A'},  # thetonstakers
    {'row': 20, 'admin': '@MEXCEnglish, @TonyStvrk, @bitcoinV2Channel, @bmxcommunity', 'community': 'N/A'},  # GemHunterrs
    {'row': 21, 'admin': '@AnoMessBot, @DevMti, @HowAllBot, @OnTopAds, @OnTopSupport, @ontopads', 'community': 'N/A'},  # OnTopTM
    {'row': 22, 'admin': '', 'community': 'N/A'},  # cryptosayer - no admin found
    {'row': 23, 'admin': '', 'community': 'N/A'}  # empty row
]

print("Starting Google Sheets update with service account...")

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
                print(f"✅ Row {update['row']} Column B updated: {update['admin']}")
            else:
                sheet.update_cell(update['row'], 2, '')  # Empty cell for no admin
                print(f"✅ Row {update['row']} Column B updated: (empty)")
            
            # Update column C (Community) - using cell reference with line breaks
            sheet.update_cell(update['row'], 3, update['community'])  # row, column number
            print(f"✅ Row {update['row']} Column C updated: {update['community']}")
            
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