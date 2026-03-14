import os
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

############# CONFIGURATION #############
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CLIENT_SECRETS_PATH = os.path.join(os.path.dirname(__file__), "..", "client_secrets.json")
TOKEN_PATH = os.path.join(os.path.dirname(__file__), "..", "token.pickle")
SPREADSHEET_ID_VAR = "SPREADSHEET_ID"
DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
VALUE_INPUT_OPTION = "RAW"
INSERT_DATA_OPTION = "INSERT_ROWS"
ERROR_MESSAGE_NO_SPREADSHEET_ID = "Spreadsheet ID not found."
#########################################

def get_credentials():
    creds = None
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_PATH, "wb") as token:
            pickle.dump(creds, token)
    return creds

def append_to_sheet(phrase: str, language: str):
    spreadsheet_id = os.getenv(SPREADSHEET_ID_VAR)
    if not spreadsheet_id:
        raise ValueError(ERROR_MESSAGE_NO_SPREADSHEET_ID)
    creds = get_credentials()
    service = build("sheets", "v4", credentials=creds)
    date = datetime.now().strftime(DATE_TIME_FORMAT)
    values = [[phrase, language, date]]
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range="A:C",
        valueInputOption=VALUE_INPUT_OPTION,
        insertDataOption=INSERT_DATA_OPTION,
        body={"values": values}
    ).execute()