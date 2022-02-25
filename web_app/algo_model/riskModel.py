
from tracemalloc import start
import pandas as pd
import numpy as np
import math
from .ticker import Ticker

# confidential level 95% for NF, 99% for the NN
class ConfidentLevel:
    NF = 1.64
    NN = 2.33

# this is the risk model to calc the VaR, and do the mote carlos simulation
# risk model takes the ticker as input, it takes many tickers as needed.
class RiskModel:

    # the *args are the tickers symbol.
    # ticker can be empty
    def __init__(self, *args):
        self.__ticker = []
        self.__pos = []
        self.__return = None
        for t in args:
            self.__ticker.append(t)

    # this is the simple return calc for the simple/ ticker
    # simple return is (p2-p1)/p1
    # future implementation can take the log normal return
    def calc_return(self, startDate, endDate):
        df = pd.DataFrame()

        for t in self.__ticker:
            t.set_data_range(startDate, endDate)
            dataReturn = t.get_data()
            df[t.get_ticker_name()] = (dataReturn['Close'] - dataReturn['Close'].shift(1)) / dataReturn['Close'].shift(1)
        self.__return = df[1:]

    # this is for setting position for the portfolio
    # to calc the risk, a position must set
    def set_position(self, *args):
        for p in args:
            self.__pos.append(p)
        if len(self.__pos) != len(self.__ticker):
            raise "Position not match the ticker in len."

    # calc VaR with XEX'
    # this is for the VaR calcuation
    def calc_VaR(self, confidentLevel):
        
        cov = self.__return.cov()
        variance = np.array(self.__pos).dot(cov).dot(np.array(self.__pos).T)
        print(variance)
        return math.sqrt(variance) * confidentLevel * -1

    #   monte carlos simulation
    def monteCarlos(self):

        # Cholesky Decomposition
        cov = self.__return.cov()
        cholesky = np.linalg.cholesky(cov)
        mean = self.__return.mean(axis=0)
        randomArray = np.random.rand(len(self.__return), len(self.__return.columns))
        df  = []
        for i in range(len(self.__return)):
            randomReturn = mean + np.transpose(cholesky.dot(np.transpose(randomArray[i])))
            df.append(randomReturn)
        df = pd.DataFrame(df)
        return df

# if __name__ == '__main__':

    # t1 = Ticker('t1')
    # t1.add_data('2021-06-01','2021-06-07',('06-01-2021',3),('06-02-2021',4),('06-03-2021',5),('06-04-2021',8),('06-05-2021',3),('06-06-2021',4),('06-07-2021',6))
    # t2 = Ticker('t2')
    # t2.add_data('2021-06-01','2021-06-07',('06-01-2021',31),('06-02-2021',42),('06-03-2021',53),('06-04-2021',85),('06-05-2021',34),('06-06-2021',46),('06-07-2021',67))

    # r = RiskModel(t1, t2)
    # r.calc_return('2021-06-01', '2021-06-07')
    # r.set_position(100, 50)
    # r.monteCarlos()