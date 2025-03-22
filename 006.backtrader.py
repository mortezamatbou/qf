import datetime
import yfinance as yf
import backtrader as bt
import pandas as pd


def yahoo_download(symbol, start, end) -> pd.DataFrame:
    ticker = yf.Ticker(symbol)
    result = ticker.history(start=start, end=end, interval='1d', auto_adjust=True)
    return pd.DataFrame(result)


class MovingAverageStrategy(bt.Strategy):

    params = (
        ('period_fast', 30),
        ('period_slow', 200),
    )

    def __init__(self):

        self.close_data = self.data.volume


        # usually this is where we create the indicators
        self.fast_sma = bt.indicators.MovingAverageSimple(self.close_data, period=self.params.period_fast)
        self.slow_sma = bt.indicators.MovingAverageSimple(self.close_data, period=self.params.period_slow)

    def next(self):
        # print("date:{} - o:{:.2f} h:{:.2f} l:{:.2f} c:{:.2f} v:{}".format(self.data.datetime.date(0), self.data.open[0], self.data.high[0], self.data.low[0], self.data.close[0], self.data.volume[0]))

        # we have to check whether we have already opened a long position
        if not self.position:
            if self.fast_sma[0] > self.slow_sma[0] and self.fast_sma[-1] < self.slow_sma[-1]:
                # print('BUY')
                self.buy()
        else:
            # check whether to close the long position
            if self.fast_sma[0] < self.slow_sma[0] and self.fast_sma[-1] > self.slow_sma[-1]:
                # print('CLOSE')
                self.close()

if __name__ == '__main__':
    cerebro = bt.Cerebro()

    start = datetime.datetime(2010,1, 1)
    end = datetime.datetime(2020, 1, 1)
    data = bt.feeds.PandasData(dataname=yahoo_download('MSFT', start, end))

    cerebro.broker.set_cash(3000)
    cerebro.broker.setcommission(0.01)
    print("Initial Capital", cerebro.broker.get_cash())

    # add data to core
    cerebro.adddata(data)
    # add strategy
    cerebro.addstrategy(MovingAverageStrategy)
    cerebro.addobserver(bt.observers.Value)
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, riskfreerate=0)
    cerebro.addanalyzer(bt.analyzers.Returns)
    cerebro.addanalyzer(bt.analyzers.DrawDown)

    # run the strategy
    result = cerebro.run()


    # evaluate the results
    print("Sharpe ratio", result[0].analyzers.sharperatio.get_analysis()['sharperatio'])
    print("Drawdown", result[0].analyzers.drawdown.get_analysis()['max']['drawdown'])
    print("Return", result[0].analyzers.returns.get_analysis()['rnorm100'])
    print("Actual Capital", cerebro.broker.getvalue(), cerebro.broker.get_cash())



