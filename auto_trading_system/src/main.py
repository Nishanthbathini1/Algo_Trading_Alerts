from data_fetcher import fetch_data
from strategy import generate_signals
from backtester import backtest
from ml_model import prepare_ml_data, train_model, predict_next_day
#from ml_model import prepare_lstm_data, train_lstm_model, evaluate_model, predict_next_day
from gsheet_logger import log_to_sheet
from telegram_alert import send_alert

stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]

for stock in stocks:
    print(f"Processing {stock}")
    data = fetch_data(stock)
    print(data.columns)
    data = generate_signals(data)
    trades = backtest(data)
    print(f"[DEBUG] {stock} - Signals: {(data['Signal']).sum()} rows with Signal=True")

    log_to_sheet(trades, f"{stock}_Trades")

    """X_train, X_test, y_train, y_test = prepare_ml_data(data)
    model, acc = train_model(X_train, X_test, y_train, y_test)"""
    (X_train, X_test, y_train, y_test), scaler, X, y = prepare_ml_data(data)
    model, acc = train_model(X_train, X_test, y_train, y_test)

    # Predict next day's move
    latest = X.iloc[-1]
    direction, confidence = predict_next_day(model, scaler, latest)
    print(f"📌 Next-day prediction for {stock}: {direction} ({confidence}% confidence)")


    print(f"{stock} model trained with {round(acc*100, 2)}% accuracy")
    #send_alert(f"{stock} model trained with {round(acc*100, 2)}% accuracy")
    if not trades.empty:
        send_alert(f"📈 Signal for {stock}!\nFirst Action: {trades.iloc[0]['Action']}\nPrice: {trades.iloc[0]['Price']:.2f}")
    else:
        send_alert(f"[⚠] No trades generated for {stock}.")

   