import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

class MovingAverageRSIStrategy:


    def __init__(self, capital, stock, start, end, short_period, long_period):
        self.data: pd.DataFrame = None
        self.is_long = False
        self.short_period = short_period
        self.long_period = long_period
        self.capital = capital
        self.equity = [capital]
        self.stock = stock
        self.start = start
        self.end = end


    def download_data(self):
        result = {}
        ticker = yf.Ticker(self.stock)
        data = ticker.history(start=self.start, end=self.end, interval='1d', auto_adjust=True)
        result['price'] = data['Close']
        self.data = pd.DataFrame(result)


    def construct_signal(self):
        self.data['short_ma'] = self.data['price'].ewm(span=self.short_period, adjust=False).mean()
        self.data['long_ma'] = self.data['price'].ewm(span=self.long_period, adjust=False).mean()

        self.data['return'] = np.log(self.data['price'] / self.data['price'].shift(1))
        self.data['move'] = self.data['price'] - self.data['price'].shift(1)

        self.data['up'] = np.where(self.data['move'] > 0, self.data['move'], 0)
        self.data['down'] = np.where(self.data['move'] < 0, self.data['move'], 0)

        # RSI
        self.data['avg_gain'] = self.data['up'].rolling(14).mean()
        self.data['avg_loss'] = self.data['down'].abs().rolling(14).mean()

        RS = self.data['avg_gain'] / self.data['avg_loss']

        self.data['rsi'] = 100.0 - (100.0 / (1.0 + RS))

        self.data = self.data.dropna()

    def simulate(self):
        # check for long or short
        price_when_buy = 0

        for index, row in self.data.iterrows():
            # close the long position we have opened
            if row['short_ma'] < row['long_ma'] and self.is_long:
                self.equity.append(self.capital * row['price'] / price_when_buy)
                self.is_long = False
            elif row['short_ma'] > row['long_ma'] and not self.is_long and row['rsi'] < 30:
                # open a long position
                price_when_buy = row['price']
                self.is_long = True

    def plot_signal(self):
        plt.figure(figsize=(12, 6))
        plt.plot(self.data['price'], label='Price')
        plt.plot(self.data['short_ma'], label='Short MA', color='blue')
        plt.plot(self.data['long_ma'], label='Long MA', color='green')
        plt.title('Moving Average Crossover Trading Strategy with RSI')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.show()


    def plot_equity(self):
        print("Profit of trading strategy: %.2f%%" % ((float(self.equity[-1]) - float(self.equity[0])) / float(self.equity[0]) * 100))
        print("Actual capital $%0.2f" % self.equity[-1])
        plt.figure(figsize=(12, 6))
        plt.xlabel("Date")
        plt.ylabel("Actual Capital ($)")
        plt.title("Equity Curve")
        plt.plot(self.equity, label="Capital", color='green')
        plt.show()

    def show_stats(self):
        print("Profit of the trading strategy: %.2f%%" % (
                (float(self.equity[-1]) - float(self.equity[0])) /
                float(self.equity[0]) * 100))
        print("Actual capital: %0.2f" % self.equity[-1])
        returns = (self.data['price'] - self.data['price'].shift(1)) / self.data['price'].shift(1)
        ratio = returns.mean() / returns.std() * np.sqrt(252)
        print('Sharpe ratio: %.2f' % ratio)


if __name__ == '__main__':
    start_date = datetime.datetime(2015, 1, 1)
    end_date = datetime.datetime(2020, 1, 1)
    strategy = MovingAverageRSIStrategy(100, "IBM", start_date, end_date, 40, 150)
    strategy.download_data()
    strategy.construct_signal()
    strategy.plot_signal()
    strategy.simulate()
    strategy.plot_equity()
    strategy.show_stats()

