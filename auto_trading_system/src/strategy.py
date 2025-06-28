from indicators import calculate_rsi, calculate_moving_averages

def generate_signals(data):
    data = calculate_rsi(data)
    data = calculate_moving_averages(data)
    data["Signal"] = (data["RSI"] < 30) & (data["20_DMA"] > data["50_DMA"])
    return data
