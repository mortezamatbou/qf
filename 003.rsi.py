import datetime
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def download(stock, start, end):
    ticker = yf.Ticker(stock)
    result = ticker.history(start=start, end=end, interval='1d', auto_adjust=True)
    data = {}
    data['price'] = result['Close']
    return pd.DataFrame(data)

data = download('IBM', '2015-01-01', '2020-01-01')

data['return'] = np.log(data['price'] / data['price'].shift(1))
data['move'] = data['price'] - data['price'].shift(1)

data['up'] = np.where(data['move'] > 0, data['move'], 0)
data['down'] = np.where(data['move'] < 0, data['move'], 0)

# RSI
data['avg_gain'] = data['up'].rolling(14).mean()
data['avg_loss'] = data['down'].abs().rolling(14).mean()

RS = data['avg_gain'] / data['avg_loss']

data['rsi'] = 100.0 - (100.0 / (1.0 + RS))

data = data.dropna()

plt.plot(data['price'], color='black')
plt.plot(data['rsi'], color='red')
plt.show()
