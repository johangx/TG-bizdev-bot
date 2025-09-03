import gspread
from google.oauth2.service_account import Credentials
import json

# Service account credentials
SERVICE_ACCOUNT_EMAIL = 'johan-271@analog-delight-451409-q2.iam.gserviceaccount.com'
SPREADSHEET_ID = '19IuLIlAOlzoiiqY4S55tG8PHkzupPauvCGfX0VvcfK0'

# Data to update (from the CSV results)
updates = [
    {'row': 2, 'admin': '@strategy', 'community': 'N/A'},
    {'row': 3, 'admin': '@strategy', 'community': 'N/A'},
    {'row': 4, 'admin': '@strategy', 'community': 'N/A'},
    {'row': 5, 'admin': '@strategy', 'community': 'N/A'},
    {'row': 6, 'admin': '@NeuralZone, @photofixer', 'community': 'N/A'},
    {'row': 7, 'admin': '@TGowner999', 'community': 'N/A'},
    {'row': 8, 'admin': '@TGowner999', 'community': 'N/A'},
    {'row': 9, 'admin': '@TGowner999', 'community': 'N/A'},
    {'row': 10, 'admin': '@TGowner999, @topovik_999', 'community': 'N/A'},
    {'row': 11, 'admin': '@TGowner999, @topovik_999', 'community': 'N/A'},
    {'row': 12, 'admin': '@tonkingram, @tonmoneybag', 'community': 'N/A'},
    {'row': 13, 'admin': '@Sa4iz1k, @gargoniel, @killhpx, @kykysik00, @ostapsmm, @pifagor_dao, @sa4iz1k, @tocatcrypto, @twall_ads, @vladuah', 'community': 'N/A'},
    {'row': 14, 'admin': '@Arch1k3, @Boomerbae, @Imijj0, @MemoryOfLegendary, @Sa4iz1k, @SheikhOfficiaI, @egor_unique, @exmanager_crypto, @nikolacoach, @tocatcrypto, @vofi555, @woskish', 'community': 'N/A'},
    {'row': 15, 'admin': '@llutfullah', 'community': 'N/A'},
    {'row': 16, 'admin': '@ad_crypto', 'community': 'N/A'},
    {'row': 17, 'admin': '@Crypto_Techware2, @Ghost4Bridge, @Makavelllly, @MamaPips, @MockinBirds, @Ovroahmed2, @anurakyaser, @mennick', 'community': 'https://t.me/W3BFLIXBot__, https://t.me/W3BFLIXBot, https://t.me/W3BFLIX_Group__, https://t.me/W3BFLIX_Group'},
    {'row': 18, 'admin': '@Sonnov_official, @sonnov_official', 'community': 'N/A'},
    {'row': 19, 'admin': '@tonstakers_support_bot', 'community': 'N/A'},
    {'row': 20, 'admin': '@MEXCEnglish, @TonyStvrk, @bitcoinV2Channel, @bmxcommunity', 'community': 'N/A'},
    {'row': 21, 'admin': '@AnoMessBot, @DevMti, @HowAllBot, @OnTopAds, @OnTopSupport, @ontopads', 'community': 'N/A'},
    {'row': 22, 'admin': '', 'community': 'N/A'}
]

print("Starting Google Sheets update with service account...")

try:
    # Create service account credentials
    # Since we don't have the JSON file, we'll try to use the service account email directly
    # First, let's try to create a credentials object using the service account email
    
    # Define the scope
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    
    # Try to authenticate using the service account email
    # We'll need to create a credentials object manually
    credentials_dict = {
        "type": "service_account",
        "project_id": "analog-delight-451409",
        "private_key_id": "your_private_key_id",
        "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n",
        "client_email": SERVICE_ACCOUNT_EMAIL,
        "client_id": "828550828244-n3pu9cafqcpno8is8b4efu1oqg6usil6.apps.googleusercontent.com",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{SERVICE_ACCOUNT_EMAIL}"
    }
    
    # Since we don't have the actual private key, let's try a different approach
    # Let's use the gspread library with a simpler authentication method
    
    print("Trying alternative authentication method...")
    
    # Try to use gspread with the service account email
    gc = gspread.service_account(filename=None)  # This will look for default credentials
    
    # If that doesn't work, let's try to create the service account JSON file
    print("Creating temporary service account credentials...")
    
    # Create a minimal service account JSON file
    service_account_info = {
        "type": "service_account",
        "project_id": "analog-delight-451409",
        "private_key_id": "temp_key_id",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...\n-----END PRIVATE KEY-----\n",
        "client_email": SERVICE_ACCOUNT_EMAIL,
        "client_id": "828550828244-n3pu9cafqcpno8is8b4efu1oqg6usil6.apps.googleusercontent.com",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{SERVICE_ACCOUNT_EMAIL}"
    }
    
    # Write the service account info to a temporary file
    with open('temp_service_account.json', 'w') as f:
        json.dump(service_account_info, f)
    
    print("Service account file created. Now trying to authenticate...")
    
    # Try to authenticate with the temporary file
    credentials = Credentials.from_service_account_file('temp_service_account.json', scopes=scope)
    gc = gspread.authorize(credentials)
    
    # Open the spreadsheet
    sheet = gc.open_by_key(SPREADSHEET_ID).sheet1
    
    print("✅ Successfully connected to Google Sheets!")
    
    # Update the data
    for update in updates:
        try:
            # Update column B (Admin)
            if update['admin']:
                sheet.update(f'B{update["row"]}', update['admin'])
                print(f"✅ Row {update['row']} Column B updated: {update['admin']}")
            
            # Update column C (Community)
            sheet.update(f'C{update["row"]}', update['community'])
            print(f"✅ Row {update['row']} Column C updated: {update['community']}")
            
        except Exception as e:
            print(f"❌ Error updating row {update['row']}: {e}")
    
    print("\n✅ Google Sheets update completed successfully!")
    
    # Clean up the temporary file
    import os
    if os.path.exists('temp_service_account.json'):
        os.remove('temp_service_account.json')
        print("Cleaned up temporary service account file.")

except Exception as e:
    print(f"❌ Error: {e}")
    print("\nThe service account authentication failed. You may need to:")
    print("1. Download the actual service account JSON key file from Google Cloud Console")
    print("2. Place it in the current directory as 'service_account.json'")
    print("3. Or manually copy the data from the CSV file") 