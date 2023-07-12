from google_sheets_connection import GoogleSheetsApi


def connect_to_gs_api():
    scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    spreadsheet_id = '1XRphnMCmqEzjdN5TTihmGWDQSQg_SgL81yxCEYz-dBk'

    conn = GoogleSheetsApi(scopes=scope,
                           spread_sheet_id=spreadsheet_id)

    return conn
