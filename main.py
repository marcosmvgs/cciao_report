import pandas as pd


def load_data():
    sheet_id = "1RFmwDvSbIsRETxJ-yiaXJwHIa_psVugbPCC1tZwukTo"
    df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
    return df





