import pandas
import numpy
from .ticker import Ticker

class TradePosition:
    Buy = 1
    Sell = -1

# this is the base stratge model. abstract the class with all the variables
class BaseStrategy:

    def __init__(self, ticker, start, end) -> None:
        self._ticker = ticker
        self._startDate = start
        self._endDate = end
        self._dataFrame = None
        self._totalPnL = 0

# moving average model from the base strategy
# it take 2 moving average row
# strategy to buy stock when the fast moving average cross to the top
# strategy to sell stock when the slow moving average cross to the top
class MovingAverageStrategy(BaseStrategy):

    def add_mv_line(self, mv1, mv2):
        df = self._ticker.get_data()
        df = df['Close'].to_frame()
        df['SMA' + str(mv1)] = df['Close'].rolling(mv1).mean()
        df['SMA' + str(mv2)] = df['Close'].rolling(mv2).mean()
        df = df.iloc[max(mv1, mv2): , :]
        df['Diff'] = (df['SMA' + str(mv1)] - df['SMA' + str(mv2)]) / abs(df['SMA' + str(mv1)] - df['SMA' + str(mv2)]) 
        df['Trade'] = numpy.sign(df['Diff']).diff().ne(0)
        df = df[['Close','Diff','Trade']]
        self._dataFrame = df
    
    # calc the pnl of this strategy
    def get_running_pnl(self):

        runPnL = []
        currPosition = 0
        totolPnL = 0
        currTrade = None
        for i, row in self._dataFrame.iterrows():
            runningPnL = 0
            if row['Trade']:
                if currPosition == 0:
                    currPosition = row['Close'] * row['Diff']
                    if row['Diff'] == 1:
                        currTrade = TradePosition.Buy
                    else:
                        currTrade = TradePosition.Sell
                else:
                    if currTrade == TradePosition.Buy:
                        runningPnL = abs(currPosition) - abs(row['Close'])
                    else:
                        runningPnL = -1 * abs(currPosition) + abs(row['Close'])
                    totolPnL += runningPnL
                    currPosition = 0
            if currPosition != 0:
                if currTrade == TradePosition.Buy:
                    runningPnL = abs(currPosition) - abs(row['Close'])
                else:
                    runningPnL = -1 * abs(currPosition) + abs(row['Close'])
            runPnL.append(runningPnL+totolPnL)

        df = pandas.DataFrame(index=self._dataFrame.index)
        df['RunningPnL'] = runPnL
        self._totalPnL = runPnL[-1]
        return df
    
    def get_total_pnl(self):
        return self._totalPnL

    # the back tester, it loop throught this strategy with the slow and fast moving average from the 5 to 5+n
    # this back tester run the strategy for different combination. iteration throught the whole population
    def run_back_tester(self, n):
        # default to run 30 days moving average back tester
        backTester = []
        for i in range(5, 5+n):
            for j in range(i+1, 5+n):
                self.add_mv_line(i, j)
                self.get_running_pnl()
                backTester.append([(i, j), self.get_total_pnl()])
        df = pandas.DataFrame(backTester, columns=['Pair', 'PnL'])
        return df

# if __name__ == '__main__':
    # t = Ticker('AAPL')
    # t.import_data_range('2021-01-01','2021-12-31')
    # t.print_data_range()

    # mv = MovingAverageStrategy(t, '2021-06-01','2021-06-30')
    # mv.add_mv_line(10, 20)
    # print(mv.run_back_tester(10))