from __future__ import print_function
import os.path
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import streamlit as st


class GoogleSheetsApi:
    def __init__(self,
                 scopes,
                 spread_sheet_id):

        self.scopes = scopes
        self.spread_sheet_id = spread_sheet_id
        self.creds = None
        self.spreadsheet = None

        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', scopes)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    r'credentials.json', scopes
                )
                self.creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
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

    def add_flight_register(self, flight_info):
        registro = self.get_sheet('Registro de Voo!A:T')
        ultima_linha = registro.shape[0] + 1

        self.spreadsheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=f'Registro de Voo!A{ultima_linha + 1}',
            valueInputOption='USER_ENTERED',
            body={'values': flight_info}
        ).execute()

    def delete_flight_register(self, flight_id):

        pass

    def update_flight_register(self, flight_id):
        pass

    def find_flight_by_id(self, flight_id):
        pass

    def find_fligth_row(self, flight_id):
        all_data = self.get_sheet('Registro de Voo!A:T')
        index_flight = all_data.index[all_data['ID'] is True]




scope = st.secrets['google_sheets']['scopes']
spreadsheet_id = st.secrets['google_sheets']['spreadsheet_id']
connection = GoogleSheetsApi(scopes=scope,
                             spread_sheet_id=spreadsheet_id)

# request_body_delete_flight_register = {
#     'requests': [
#         {
#             'deleteRange': {
#                 'range': {
#                     "sheetId": 2088240049,
#                     "startRowIndex": 1,
#                     "endRowIndex": 2
#                 },
#                 'shiftDimension': 'ROWS'
#             }
#         }
#     ]
# }
#
# connection.spreadsheet.batchUpdate(
#     spreadsheetId=spreadsheet_id,
#     body=request_body_delete_flight_register
# ).execute()
registros = connection.get_sheet('Registro de Voo!A:T')
index_flight = registros.index[registros['ID'] == 'marcos']
print(registros)
print(index_flight + 2)
