import yfinance as yf
import pandas as pd

#1 step 1 : get data

ticker = input("Enter stock ticker: ")
data = yf.download(ticker, period="6mo")
#data =yf.download("INFY.NS",period="6mo")

#calculate moving averages
data ['MA10']=data['Close'].rolling(window=10).mean()
data ['MA50']=data['Close'].rolling(window=50).mean()

#create signal
data.loc[data['MA10']>data['MA50'],'signal']=1
data.loc[data['MA10']<data['MA50'],'signal']=-1

data['position'] = data['signal'].diff()

print(data[['Close', 'MA10', 'MA50', 'signal', 'position']].tail(30))


last_signal = data['position'].iloc[-1]

if last_signal == 2:
    print("BUY signal triggered")
elif last_signal == -2:
    print("SELL signal triggered")
else:
    print("No new signal")

# RSI Calculation
delta = data['Close'].diff()

gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()

rs = gain / loss
data['RSI'] = 100 - (100 / (1 + rs))

last_position = data['position'].iloc[-1]
last_rsi = data['RSI'].iloc[-1]

print("RSI of ",ticker," = ",last_rsi)
if last_position == 2 and last_rsi < 70:
    print("BUY (confirmed by RSI)")
elif last_position == -2 and last_rsi > 30:
    print("SELL (confirmed by RSI)")
else:
    print("No strong signal") 


