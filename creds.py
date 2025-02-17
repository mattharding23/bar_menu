import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets Setup
def get_google_sheet():
    # Authenticate and open the Google Spreadsheet
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    print("Current Working Directory:", os.getcwd())
    creds = ServiceAccountCredentials.from_json_keyfile_name("bar-menu-448602-586e39802c4c.json", scope)
    client = gspread.authorize(creds)
    return client.open("Bar Menu")  # Replace with your spreadsheet name