import backtrader as bt
import datetime
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt


def yahoo_download(symbol, start, end) -> pd.DataFrame:
    ticker = yf.Ticker(symbol)
    result = ticker.history(start=start, end=end, interval='1d', auto_adjust=True)
    return pd.DataFrame(result)


def calculate_atr(data: pd.DataFrame):
    high_low = data['High'] - data['Low']
    high_close = np.abs(data['High'] - data['Close'].shift(1))
    low_close = np.abs(data['Low'] - data['Close'].shift(1))
    
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_ranges = np.max(ranges, axis=1)
    # atr = true_ranges.rolling(14).sum() / 14
    return true_ranges.rolling(14).mean()


if __name__ == '__main__':
    start_date = datetime.datetime(2011, 3, 31)
    end_date = datetime.datetime(2013, 1, 1)

    stock_data = yahoo_download('XOM', start_date, end_date)
    atr = calculate_atr(stock_data)
    fig, (ax1, ax2) = plt.subplots(2)
    fig.suptitle("Stock Price and ATR Indicator")
    ax1.plot(stock_data['Close'])
    ax2.plot(atr)
    plt.show()