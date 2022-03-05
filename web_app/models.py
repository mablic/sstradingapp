from ast import Mod
from tracemalloc import start
from turtle import position
from django.db import models

from web_app.algo_model import riskModel, ticker

from .algo_model import *
from .mongoDB import mongoDB
from .message import message
import pandas as pd
# Create your models here.


class Model:

    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance
    
    def __init__(self) -> None:
        self.DB = mongoDB.MongoDB()
        self.DB.connect_to_db()
        self.ticker = None
        self.graph = None
        self.riskModel = None
        self.email = message.Email()
    
    def get_db(self):
        return self.DB

    # download the ticker from the mongoDB database
    def get_all_ticker_from_db(self):
        wikiData = importData.Data()
        wikiData.read_wiki()
        allTicker = wikiData.get_all_ticker()
        currTicker = self.DB.get_all_ticker_from_db()
        allTicker.sort()
        currTicker.sort()

        for i in range(len(currTicker)):
            for j in range(len(allTicker)):
                if currTicker[i] == allTicker[j]:
                    allTicker[:] = allTicker[:j] + allTicker[j+1:]
                    break

        if currTicker == []:
            currTicker = []
        else:
            currTicker = ['Database List'] + ['------------'] + currTicker
        result = currTicker + ['------------'] + ['S&P 500 List'] + ['------------'] + allTicker
        return result

    # This will print the baisc graph as pic into the web page.
    def run_base_graph(self, tickerName, startDate, endDate, chartType='line'):
        g = graphData.GraphData()
        t = ticker.Ticker(tickerName)
        if self.DB.find_ticker_from_db(tickerName):
            data = self.DB.find_data_from_db(tickerName)
            df = pd.DataFrame(list(data))
            t.add_data_from_database(df)
            t.set_data_range(startDate, endDate)
        else:
            t.import_data_range(startDate, endDate)
            self.DB.insert_to_db(t)
        g.set_data(t, t.get_start_date(), t.get_end_date(), chartType)
        self.graph = g
        g.graph_plot()

    # VaR calculation will need the VaR model from the algo folder
    def get_VaR_value(self, startDate, endDate, tickers, positions):
        if tickers == [] or positions == []:
            raise "No position or ticker"
        # remove duplicate tickers and aggregate the position if any dup
        tickerDict = {}
        for i in range(len(tickers)):
            if tickers[i] in tickerDict.keys():
                tickerDict[tickers[i]] += positions[i]
            else:
                tickerDict[tickers[i]] = positions[i]
        self.riskModel = riskModel.RiskModel()
        positions = []
        for tickerName, p in tickerDict.items():
            t = ticker.Ticker(tickerName)
            if self.DB.find_ticker_from_db(tickerName):
                data = self.DB.find_data_from_db(tickerName)
                df = pd.DataFrame(list(data))
                t.add_data_from_database(df)
                t.set_data_range(startDate, endDate)
            else:
                t.import_data_range(startDate, endDate)
                self.DB.insert_to_db(t)       
            self.riskModel.set_ticker(t)
            positions.append(p)

        self.riskModel.set_position(*positions)
        return self.riskModel.calc_VaR()

    # send email to me
    def send_email(self, name, subject, fromEmail, msg):
        self.email.send_email(name, subject, fromEmail, msg)


# if __name__ == '__main__':

#     m = Model()
#     # g = graphData.GraphData()
#     t = ticker.Ticker('AAPL')
#     t.import_data_range('2021-01-01', '2021-12-31')
#     m.get_VaR_value('2021-01-01', '2021-12-31',['AAPL', 'A'], [100,150])
    # data = m.get_db().find_data_from_db('AAPL')
    # df = pd.DataFrame(list(data))
    # t.add_data_from_database(df)
    # t.set_data_range('2021-01-01', '2021-12-31')
    # g.set_data(t, t.get_start_date(), t.get_end_date(), 'line')
    # g.graph_plot()

