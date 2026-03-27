import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# ======================
# DATA FETCH
# ======================
def get_data(ticker):
    data = yf.download(ticker, period="6mo")

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    return data


# ======================
# INDICATORS
# ======================
def add_moving_averages(data):
    data['MA10'] = data['Close'].rolling(10).mean()
    data['MA50'] = data['Close'].rolling(50).mean()
    return data


def add_rsi(data):
    delta = data['Close'].diff()

    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()

    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

    return data


# ======================
# STATE-BASED SIGNAL LOGIC
# ======================
def generate_signal(data):
    data['Signal'] = 0

    for i in range(1, len(data)):
        prev_signal = data['Signal'].iloc[i-1]

        ma10 = data['MA10'].iloc[i]
        ma50 = data['MA50'].iloc[i]
        rsi = data['RSI'].iloc[i]

        # ENTRY condition
        if prev_signal == 0 and ma10 > ma50 and 40 < rsi < 70:
            data.iloc[i, data.columns.get_loc('Signal')] = 1

        # EXIT condition
        elif prev_signal == 1 and (ma10 < ma50 or rsi < 40):
            data.iloc[i, data.columns.get_loc('Signal')] = 0

        # HOLD condition
        else:
            data.iloc[i, data.columns.get_loc('Signal')] = prev_signal

    # Track changes
    data['Position'] = data['Signal'].diff()

    return data


# ======================
# DECISION
# ======================
def decision(data):
    last_signal = data['Signal'].iloc[-1]

    if last_signal == 1:
        return "BUY / HOLD"
    else:
        return "OUT / SELL"


# ======================
# MAIN
# ======================
ticker = input("Enter stock: ")

data = get_data(ticker)
data = add_moving_averages(data)
data = add_rsi(data)

# Remove NaNs
data = data.dropna()

data = generate_signal(data)

# ======================
# OUTPUT
# ======================
print("Decision:", decision(data))

print("\n--- Indicator Data ---")
print(data[['Close', 'MA10', 'MA50', 'RSI', 'Signal', 'Position']].tail(30))

# ======================
# BACKTEST
# ======================
data['Market_Return'] = data['Close'].pct_change()

# Use signal (no cheating)
data['Strategy_Return'] = data['Market_Return'] * data['Signal'].shift(1)

data['Cumulative_Market'] = (1 + data['Market_Return']).cumprod()
data['Cumulative_Strategy'] = (1 + data['Strategy_Return']).cumprod()

print("\n--- Performance ---")
print(data[['Cumulative_Market', 'Cumulative_Strategy']].tail(30))

# Final returns
total_market_return = data['Cumulative_Market'].iloc[-1] - 1
total_strategy_return = data['Cumulative_Strategy'].iloc[-1] - 1

print(f"\nMarket Return: {total_market_return:.2%}")
print(f"Strategy Return: {total_strategy_return:.2%}")

# ======================
# PLOT
# ======================
data[['Cumulative_Market', 'Cumulative_Strategy']].plot()
plt.title(f"{ticker} Strategy vs Market")
plt.show()