import pandas as pd

def calculate_rsi(data, period=14):
    delta = data["Close"].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss

    data["RSI"] = 100 - (100 / (1 + rs))
    return data

def calculate_moving_averages(data):
    data["20_DMA"] = data["Close"].rolling(window=20).mean()
    data["50_DMA"] = data["Close"].rolling(window=50).mean()
    return data
