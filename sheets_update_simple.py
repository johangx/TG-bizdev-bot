import requests
import json

# Google Sheets API key and spreadsheet ID
API_KEY = 'AIzaSyDcRJlmoKjWmofFzntOcHRBF-H8_fzieUg'
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

print("Starting Google Sheets update...")

# Try using the Google Sheets API with a different approach
try:
    # First, let's try to read the sheet to verify access
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/A1:C25?key={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        print("✅ Successfully connected to Google Sheets!")
        
        # Now try to update using the update method
        for update in updates:
            try:
                # Update column B (Admin)
                if update['admin']:
                    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/B{update['row']}?valueInputOption=USER_ENTERED&key={API_KEY}"
                    data = {"values": [[update['admin']]]}
                    response = requests.put(url, json=data)
                    if response.status_code == 200:
                        print(f"✅ Row {update['row']} Column B updated: {update['admin']}")
                    else:
                        print(f"❌ Row {update['row']} Column B failed: {response.status_code}")
                
                # Update column C (Community)
                url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/C{update['row']}?valueInputOption=USER_ENTERED&key={API_KEY}"
                data = {"values": [[update['community']]]}
                response = requests.put(url, json=data)
                if response.status_code == 200:
                    print(f"✅ Row {update['row']} Column C updated: {update['community']}")
                else:
                    print(f"❌ Row {update['row']} Column C failed: {response.status_code}")
                
            except Exception as e:
                print(f"❌ Error updating row {update['row']}: {e}")
        
        print("\n✅ Google Sheets update completed!")
        
    else:
        print(f"❌ Cannot access Google Sheets: {response.status_code}")
        print("Response:", response.text)

except Exception as e:
    print(f"❌ Error: {e}")
    print("\nThe Google Sheets API requires proper authentication. You may need to:")
    print("1. Set up a service account with proper credentials")
    print("2. Or use OAuth2 authentication")
    print("3. Or manually copy the data from the CSV file") 