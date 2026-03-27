import yfinance as yf
data = yf.download("RELIANCE.NS",period="5D")
print(data.tail())
data['Return'] = data['Close'].pct_change()
print(data[['Close', 'Return']].tail())

data = yf.download("TCS.NS",period="5D")
print(data.tail())
data['Return'] = data['Close'].pct_change()
print(data[['Close', 'Return']].tail())

data = yf.download("INFY.NS",period="5D")
print(data.tail())
data['Return'] = data['Close'].pct_change()
print(data[['Close', 'Return']].tail())

