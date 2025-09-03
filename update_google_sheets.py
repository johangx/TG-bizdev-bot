import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv

# Google Sheets API setup
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
gc = gspread.authorize(credentials)

# Open the spreadsheet
spreadsheet_id = '19IuLIlAOlzoiiqY4S55tG8PHkzupPauvCGfX0VvcfK0'
sheet = gc.open_by_key(spreadsheet_id).sheet1

# Read the CSV results
results = []
with open('channel_admins_results.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        results.append(row)

# Update the Google Sheets
for i, result in enumerate(results, start=2):  # Start from row 2 (skip header)
    # Column B: Admin handles
    admin_handles = result['Admins (comma-separated)']
    if admin_handles:
        sheet.update(f'B{i}', admin_handles)
    
    # Column C: Community chat links
    community_links = result['Community Chat Links']
    if community_links:
        sheet.update(f'C{i}', community_links)
    else:
        sheet.update(f'C{i}', 'N/A')

print("Google Sheets updated successfully!") 