import datetime
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

symbol = 'BTC-USD'
start = datetime.datetime(2025, 3, 1, 12, 0, 0)
end = datetime.datetime(2025, 3, 1, 22, 0, 0)
interval = '5m'

ticker = yf.Ticker(symbol)
data = ticker.history(start=start, end=end, interval=interval)

mpf.plot(data, type='candle', volume=True, mav=(20,5), title = symbol, tight_layout=True, figratio=(10,5))