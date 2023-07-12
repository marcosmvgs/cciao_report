from __future__ import print_function
import os.path
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleSheetsApi:
    def __init__(self,
                 scopes,
                 spread_sheet_id):

        self.scopes = scopes
        self.spread_sheet_id = spread_sheet_id
        self.creds = None
        self.spreadsheet = None

        if os.path.exists('api_gs/token.json'):
            self.creds = Credentials.from_authorized_user_file('api_gs/token.json', scopes)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    r'api_gs/credentials.json', scopes
                )
                self.creds = flow.run_local_server(port=0)
            with open('api_gs/token.json', 'w') as token:
                token.write(self.creds.to_json())
        try:
            service = build('sheets', 'v4', credentials=self.creds)
            self.spreadsheet = service.spreadsheets()
        except HttpError as err:
            print(err)
            self.spreadsheet = None

    def get_sheet(self, sheet_name):
        result = self.spreadsheet.values().get(spreadsheetId=self.spread_sheet_id,
                                               range=sheet_name).execute()
        values = result.get('values', [])
        data = pd.DataFrame(columns=values[0], data=values[1:])
        return data
