import pandas as pd

def backtest(data, investment=20000):
    data = data.copy()
    position = False
    buy_price = 0
    trades = []

    for i in range(1, len(data)):
        if data["Signal"].iloc[i] and not position:
            buy_price = data["Close"].iloc[i]
            position = True
            trades.append({"Date": data["Date"].iloc[i], "Action": "BUY", "Price": buy_price})
        elif position and data["RSI"].iloc[i] > 70:
            sell_price = data["Close"].iloc[i]
            profit = (sell_price - buy_price) / buy_price * 100
            trades.append({"Date": data["Date"].iloc[i], "Action": "SELL", "Price": sell_price, "Profit %": round(profit, 2)})
            position = False

    return pd.DataFrame(trades)
