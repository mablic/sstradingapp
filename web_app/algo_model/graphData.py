#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib2to3.pgen2.pgen import DFAState
from matplotlib import ticker
import pandas as pd
import os
import mplfinance as mpf
from datetime import datetime
import matplotlib.pyplot as plt
from .ticker import Ticker
from .strategyModel import MovingAverageStrategy

# Type for the chart
class PlotType:
    candle = 'candle'
    line = 'line'
    renko = 'renko'
    pnf = 'pnf'
    ohlc = 'ohlc'

class GraphData:
    
    # GraphData class only graph the base
    # This is the base class for the child class
    def __init__(self) -> None:
        self.__ticker = None
        self.__startDate = '1990-01-01'
        self.__endDate = '1990-01-01'
        plt.switch_backend('Agg')

    # set the chart data, it takes the start date, end date and the type as optional from the Type class above
    def set_data(self, ticker, start, end, type='line'):
        format = "%Y-%m-%d"
        try:
            self.__ticker = ticker
            datetime.strptime(start, format)
            datetime.strptime(end, format)
            self.__startDate = start
            self.__endDate = end
            self.__type = type
        except ValueError:
            raise print("Invalid input for the datetime. It should be YYYY-MM-DD")

    def get_plot_base(self):
        return self.__ticker, self.__type

    def graph_plot(self):
        if not self.__ticker.check_if_has_data():
            self.__ticker.import_data_range(self.__startDate, self.__endDate)
        else:
            self.__ticker.set_data_range(self.__startDate, self.__endDate)
        filename = os.getcwd() + '/static/images/pic.png'
        # print('graph: start date='+self.__startDate + '; enddate=' + self.__endDate + '; chart type=' + self.__type)
        mpf.plot(self.__ticker.get_data(), type=self.__type, volume=True, savefig=dict(fname=filename,dpi=150,pad_inches=0.25))
    
    def graph_pnl(self, df):
        plt.plot(df)
        plt.show()

# this is a child class for the GraphData class
# this is a base class for further graphing, example moving average
# future implementation can take places from this base class
class DecoratorGraph(GraphData):

    def __init__(self, graphData) -> None:
        super().__init__()
        self._graphData = graphData
        self._ticker, self._type = graphData.get_plot_base()

# this is a child class for the GraphData class
# this class plot the chart with the moving average line
class DecoratorMV(DecoratorGraph):
    
    def set_plot(self, graphData) -> None:
        super().__init__(graphData)
        self.__mv = []

    # this is for adding mvoing average line into the chart
    def add_mv(self, mv):
        self.__mv.append(mv)

    # plot the chart with the overwrittern class of the base class
    def graph_plot(self):
        mpf.plot(self._ticker.get_data(), type=self._type, mav=tuple(self.__mv), volume=True)

# if __name__ == '__main__':

#     t = Ticker('AAPL')
#     t.import_data_range('2021-01-01','2021-12-31')
#     t.print_data_range()

#     g = GraphData()
#     g.set_data(t, '2021-01-01','2021-12-31')
#     g.graph_plot()

    # mv = DecoratorMV(g)
    # mv.set_plot(g)
    # mv.add_mv(3)
    # mv.add_mv(5)
    # # mv.graph_plot()

    # mv = MovingAverageStrategy(t, '2021-01-01','2021-12-31')
    # df = mv.run_back_tester(10)