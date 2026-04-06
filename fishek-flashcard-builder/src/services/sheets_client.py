import os
from datetime import datetime
from pathlib import Path
import sys
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

def get_config_dir():
    if sys.platform == "win32":
        return os.path.join(os.environ.get("APPDATA", ""), "fishek")
    return os.path.join(os.path.expanduser("~"), ".config", "fishek")

CONFIG_DIR = get_config_dir()

def get_token_path():
    if getattr(sys, 'frozen', False):
        return Path(CONFIG_DIR) / "token.pickle"
    return Path(__file__).resolve().parents[2] / "token.pickle"

def get_client_secrets_path():
    if getattr(sys, "frozen", False):
        return Path(CONFIG_DIR) / "client_secrets.json"
    return Path(__file__).resolve().parents[2] / "client_secrets.json"

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), "..", relative_path)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CLIENT_SECRETS_PATH = get_client_secrets_path()
TOKEN_PATH = get_token_path()
SPREADSHEET_ID_VAR = "SPREADSHEET_ID"
RANGE_NAME = "A:C"
ERROR_MESSAGE_NO_SPREADSHEET_ID = "Spreadsheet ID not found."

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

def get_sheet_data():
    spreadsheet_id = os.getenv(SPREADSHEET_ID_VAR)
    
    if not spreadsheet_id:
        raise ValueError(ERROR_MESSAGE_NO_SPREADSHEET_ID)
    
    creds = get_credentials()
    service = build("sheets", "v4", credentials=creds)

    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=RANGE_NAME)
        .execute()
    )
    
    values = result.get("values", [])

    if not values:
        return []
    
    header = values[0]

    if header == ["word", "language", "created"]:
        values = values[1:]

    return values