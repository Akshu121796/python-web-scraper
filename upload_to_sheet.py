import gspread
from google.oauth2.service_account import Credentials
import pandas as pd


CREDENTIALS_FILE = "credentials.json"

# Your Google Sheet name
SPREADSHEET_NAME = "SearchIQS Ashford Land Records"

CSV_FILE = "sample_output.csv"


def upload_to_google_sheets():

    print("Connecting to Google Sheets...")

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    credentials = Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=scopes
    )

    client = gspread.authorize(credentials)

    # Open the spreadsheet
    spreadsheet = client.open(SPREADSHEET_NAME)

    # Use the first worksheet
    worksheet = spreadsheet.sheet1

    # Read CSV
    df = pd.read_csv(CSV_FILE)

    # Clear existing data
    worksheet.clear()

    # Convert dataframe to rows
    data = [df.columns.tolist()] + df.fillna("").values.tolist()

    # Upload
    worksheet.update(
        range_name="A1",
        values=data
    )

    print("Upload successful!")
    print(f"Rows uploaded: {len(df)}")

    print()
    print("Google Sheet:")
    print(spreadsheet.url)


if __name__ == "__main__":
    upload_to_google_sheets()