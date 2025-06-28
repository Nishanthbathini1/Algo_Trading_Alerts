import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from config import GOOGLE_SHEET_ID

def connect_sheet():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('../google_creds.json', scope)
    client = gspread.authorize(creds)
    return client.open_by_key(GOOGLE_SHEET_ID)

def log_to_sheet(data, sheet_name):
    spreadsheet = connect_sheet()

    # 🔒 Convert Series to DataFrame if needed
    if isinstance(data, pd.Series):
        df = data.to_frame().T
    elif isinstance(data, dict):
        df = pd.DataFrame([data])
    else:
        df = data.copy()

    # 🔐 If empty, don't update sheet
    if df.empty:
        print(f"[INFO] No data to write for sheet: {sheet_name}")
        return

    # 🧽 Convert datetime and all types to string for Google Sheets
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]) or isinstance(df[col].iloc[0], pd.Timestamp):
            df[col] = df[col].astype(str)

    df = df.astype(str)

    # 🧾 Connect or create the sheet tab
    try:
        sheet = spreadsheet.worksheet(sheet_name)
    except gspread.exceptions.WorksheetNotFound:
        sheet = spreadsheet.add_worksheet(title=sheet_name, rows="1000", cols="20")

    sheet.clear()

    # ✏ Update sheet
    sheet.update([df.columns.tolist()] + df.values.tolist())
    print(f"[✅] Sheet '{sheet_name}' updated successfully.")