
import pandas as pd
import numpy as np
import math
from .ticker import Ticker
from tracemalloc import start
from enum import Enum

# confidential level 95% for NF, 99% for the NN
class ConfidentLevel(Enum):
    NF = 1.64
    NN = 2.33

# this is the risk model to calc the VaR, and do the mote carlos simulation
# risk model takes the ticker as input, it takes many tickers as needed.
class RiskModel:

    # the *args are the tickers symbol.
    # ticker can be empty
    def __init__(self):
        self.__ticker = []
        self.__pos = []
        self.__return = None

    # this is the simple return calc for the simple/ ticker
    # simple return is (p2-p1)/p1
    # future implementation can take the log normal return
    def calc_return(self):
        df = pd.DataFrame()

        for t in self.__ticker:
            # t.set_data_range(startDate, endDate)
            dataReturn = t.get_data()
            # print(dataReturn)
            df[t.get_ticker_name()] = (dataReturn['Close'] - dataReturn['Close'].shift(1)) / dataReturn['Close'].shift(1)
            # print(df[t.get_ticker_name()])
        # print(df[1:])
        self.__return = df[1:]

    # this is for appending ticker into the model
    def set_ticker(self, ticker):
        self.__ticker.append(ticker)
        self.__pos.append(ticker.get_last_close_data())

    # this is for setting position for the portfolio
    # to calc the risk, a position must set
    def set_position(self, *args):
        for i in range(len(args)):
            # print(self.__pos[i])
            self.__pos[i] *= float(args[i])
        # print(args)
        # print(self.__pos)
        # print(self.__ticker)
        if len(self.__pos) != len(self.__ticker):
            raise "Position not match the ticker in len."

    # calc VaR with XEX'
    # this is for the VaR calcuation
    def calc_VaR(self):
        
        self.calc_return()
        varList = []
        cov = self.__return.cov()
        # print(cov)
        # print(self.__pos)
        variance = np.array(self.__pos).dot(cov).dot(np.array(self.__pos).T)
        # print(variance)
        for c in ConfidentLevel:
            varList.append(math.sqrt(variance) * c.value * -1)
        return varList

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

#     t1 = Ticker('AAPL')
#     t1.import_data_range('2021-01-01','2021-06-30')
#     t2 = Ticker('A')
#     t2.import_data_range('2021-01-01','2021-06-30')

#     r = RiskModel()
#     r.set_ticker(t1)
#     r.set_ticker(t2)
#     r.calc_return('2021-06-01', '2021-06-30')
#     r.set_position(100, 50)
#     print(r.calc_VaR())