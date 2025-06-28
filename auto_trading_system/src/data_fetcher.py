import yfinance as yf
import time
import pandas as pd

def fetch_data(ticker, period="30mo", interval="1d", retries=3):
    for attempt in range(retries):
        try:
            data = yf.download(ticker, period=period, interval=interval)
            if not data.empty:
                # ✅ Flatten MultiIndex columns if present
                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]

                data.reset_index(inplace=True)
                return data
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
        time.sleep(2)
    raise ValueError(f"Failed to fetch data for {ticker} after {retries} attempts.")