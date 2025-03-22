import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import datetime


def download_data(stock, start, end):
    data = {}
    ticker = yf.Ticker(stock)
    ticker = ticker.history(start=start, end=end, interval='1d')
    data['Price'] = ticker['Close']
    return pd.DataFrame(data)


def construct_signals(data: pd.DataFrame, short_period: int, long_period: int):
    signals = data.copy(deep=True)
    signals['Short EMA'] = data['Price'].ewm(span=short_period, adjust=False).mean()
    signals['Long EMA'] = data['Price'].ewm(span=long_period, adjust=False).mean()
    signals.dropna(inplace=True)
    return signals


def plot_data(data):
    plt.figure(figsize=(12, 6))
    plt.plot(data['Price'], label='Price', color='black')
    plt.plot(data['Short EMA'], label='Short MA', color='blue')
    plt.plot(data['Long EMA'], label='Long MA', color='red')
    plt.title('Exponential Moving Average (EMA) Indicators')
    plt.xlabel('Date')
    plt.ylabel('Date')
    plt.show()

if __name__ == '__main__':

    start_date = datetime.datetime(2010, 1, 1)
    end_date = datetime.datetime(2020, 1, 1)

    stock_data = download_data("IBM", start_date, end_date)
    data = construct_signals(stock_data, 50, 200)
    print(data)
    plot_data(data)



