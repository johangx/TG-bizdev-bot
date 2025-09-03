import gspread
from google.oauth2.service_account import Credentials
import json

# Try to access the sheet directly
try:
    # Open the spreadsheet by ID
    spreadsheet_id = '19IuLIlAOlzoiiqY4S55tG8PHkzupPauvCGfX0VvcfK0'
    
    # Try to open without credentials first (if sheet is public)
    gc = gspread.service_account()
    sheet = gc.open_by_key(spreadsheet_id).sheet1
    
    print("Successfully connected to Google Sheets!")
    
    # Data to update
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
    
    # Update the sheet
    for update in updates:
        try:
            # Update column B (Admin)
            if update['admin']:
                sheet.update(f'B{update["row"]}', update['admin'])
                print(f"Updated row {update['row']} Column B: {update['admin']}")
            
            # Update column C (Community)
            sheet.update(f'C{update["row"]}', update['community'])
            print(f"Updated row {update['row']} Column C: {update['community']}")
            
        except Exception as e:
            print(f"Error updating row {update['row']}: {e}")
    
    print("Google Sheets updated successfully!")
    
except Exception as e:
    print(f"Error accessing Google Sheets: {e}")
    print("The sheet may need to be set to 'Anyone with the link can edit' for this to work.") 