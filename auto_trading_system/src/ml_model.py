import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
import ta

def add_features(data):
    data = data.copy()
    # Technical indicators
    data["RSI"] = ta.momentum.RSIIndicator(data["Close"]).rsi()
    macd = ta.trend.MACD(data["Close"])
    data["MACD"] = macd.macd()
    data["MACD_signal"] = macd.macd_signal()
    data["Momentum"] = ta.momentum.stochrsi(data["Close"])
    data["20_DMA"] = data["Close"].rolling(20).mean()
    data["50_DMA"] = data["Close"].rolling(50).mean()
    data["EMA_9"] = data["Close"].ewm(span=9).mean()
    data["Price_Change"] = data["Close"].pct_change(5)
    data["Volatility"] = data["Close"].rolling(10).std()
    data["OBV"] = (np.sign(data["Close"].diff()) * data["Volume"]).fillna(0).cumsum()
    data["ROC"] = ta.momentum.ROCIndicator(close=data["Close"]).roc()
    
   
    data.dropna(inplace=True)
    return data

def prepare_ml_data(data):
    data = add_features(data)
    # Define target: 1 if tomorrow's close > today's close, else 0
    data["Target"] = (data["Close"].shift(-5) > data["Close"]).astype(int)
    future_return = (data["Close"].shift(-5) - data["Close"]) / data["Close"]
    data["Target"] = (future_return > 0.01).astype(int)  # Predict UP only if return > 1%

    data.dropna(inplace=True)

    features = ["RSI", "MACD", "MACD_signal", "Momentum", "20_DMA", "50_DMA", "EMA_9", "OBV", "ROC", "Volume", "Price_Change", "Volatility",]
    
    X = data[features]
    y = data["Target"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y), scaler, X, y

def train_model(X_train, X_test, y_train, y_test):
    model = XGBClassifier(
        n_estimators=250,
        learning_rate=0.05,
        max_depth=5,
        subsample=0.8,
        colsample_bytree=0.8,
        use_label_encoder=False,
        eval_metric="logloss",
        random_state=42
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    roc = roc_auc_score(y_test, model.predict_proba(X_test)[:,1])
    
    print(f"[🔍] ROC-AUC Score: {round(roc, 2)}")
    print("[📊] Classification Report:")
    print(classification_report(y_test, preds))

    return model, acc

def predict_next_day(model, scaler, latest_row):
    latest_scaled = scaler.transform([latest_row])
    pred = model.predict(latest_scaled)[0]
    prob = model.predict_proba(latest_scaled)[0]
    return "UP" if pred == 1 else "DOWN", round(max(prob) * 100, 2)