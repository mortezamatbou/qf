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
    signals['Short MA'] = data['Price'].rolling(window=short_period).mean()
    signals['Long MA'] = data['Price'].rolling(window=long_period).mean()
    signals.dropna(inplace=True)
    return signals


def plot_data(data):
    plt.figure(figsize=(12, 6))
    plt.plot(data['Price'], label='Price', color='black')
    plt.plot(data['Short MA'], label='Short MA', color='blue')
    plt.plot(data['Long MA'], label='Long MA', color='red')
    plt.title('Moving Average (MA) Indicators')
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



