# Algo_Trading_Alerts
# 📈 Smart Algorithmic Trading System using ML + Telegram Alerts

An intelligent trading assistant that fetches real-time stock data, analyzes it using technical indicators, predicts price direction using machine learning, and sends buy/sell alerts via Telegram — fully automated and customizable!

---

## 🚀 Features

- 📉 Real-time Stock Data (via Yahoo Finance)
- 📊 Technical Indicators: RSI, MACD, Momentum, Moving Averages (20DMA, 50DMA), EMA
- 🤖 Machine Learning Models: Logistic Regression, Decision Tree, Random Forest
- 📈 Predicts Next-Day Stock Movement: `UP` / `DOWN` with confidence score
- 📬 Telegram Alerts for buy signals or ML-based recommendations
- 🧠 Modular Design for easy customization, expansion, and scheduling

---

## 🗂️ Project Structure

algo_trading_system/
├── src/
│ ├── data_fetcher.py # Downloads stock data
│ ├── indicators.py # Computes RSI, MACD, moving averages
│ ├── strategy.py # Generates rule-based trading signals
│ ├── ml_model.py # ML feature engineering + prediction
│ ├── telegram_alert.py # Sends Telegram notifications
│ ├── sheet_logger.py # (Optional) Logs trades to Google Sheets
│ └── config.py # Stores API tokens
├── main.py # Runs full pipeline
├── creds.json # Google Sheets API credentials
├── requirements.txt # Python dependencies
└── README.md # You're here!

yaml
Copy
Edit

---

## 🛠️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/algo_trading_system.git
cd algo_trading_system
2️⃣ Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
3️⃣ Configure API Keys
Create a file src/config.py:

python
Copy
Edit
# src/config.py
TELEGRAM_BOT_TOKEN = "your_bot_token"
TELEGRAM_CHAT_ID = "your_chat_id"
(Optional): Add creds.json to use Google Sheets logging. Create it from your Google Cloud Console.

🧠 How It Works
Data Fetching
Gets 2 years of daily price data from Yahoo Finance for any given stock (e.g., RELIANCE.NS).

Feature Engineering
Calculates:

RSI

MACD and MACD Signal Line

Momentum

20DMA, 50DMA, EMA(9)

Volume and Daily Price Change %

ML Model Training

Splits the data

Trains on historical patterns

Predicts next-day direction

Supports Random Forest, Decision Tree, Logistic Regression

Rule-Based Signal Generation

RSI < 30 (oversold)

20DMA > 50DMA (bullish crossover)

Alert & Logging

Sends buy signal or prediction via Telegram

(Optional) Logs decision to Google Sheets

🧪 Example Output
csharp
Copy
Edit
[📡] Fetching data for RELIANCE.NS...
[✅] Sheet 'RELIANCE.NS_Trades' updated successfully.
[🔍] ML Prediction: UP with 78.6% confidence
[📈] Buy Signal Confirmed (RSI < 30 and 20DMA > 50DMA)
[📬] Telegram alert sent!
🔍 Models Used
Logistic Regression

Decision Tree

Random Forest (Default)

All trained using scikit-learn. Accuracy and classification report printed at each run.

▶️ Run the App
bash
Copy
Edit
python main.py
To automate it daily, use CRON (Linux/macOS) or Task Scheduler (Windows).

📬 Telegram Bot Setup
Search @BotFather on Telegram

Create a bot → Save the bot token

Visit:

bash
Copy
Edit
https://api.telegram.org/bot<your_token>/getUpdates
Send a message to your bot and fetch your chat_id

Paste both token and ID in config.py

💡 Future Ideas
Candlestick pattern detection

LSTM or GRU-based prediction models

Web dashboard for alerts and analytics

Stop-loss & target integration

Multiple stock scanning with priorities

📄 License
MIT License – Free to use, modify, and contribute!

👨‍💻 Author
Nishanth Bathini
Final Year CSE (AI & ML)
Vasavi College of Engineering
📬 Passionate about FinTech, AI, and Automation
