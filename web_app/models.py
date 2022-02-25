from ast import Mod
from tracemalloc import start
from django.db import models

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
        self.email = message.Email()
    
    def get_db(self):
        return self.DB

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

    def run_base_graph(self, tickerName, startDate, endDate, chartType='line'):
        # print(tickerName)
        # print(self.DB.find_ticker_from_db(tickerName))
        # print('ticker='+tickerName+'startDate='+startDate+'endDate='+endDate+'chartType='+chartType)
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
        # print('MODELS--------------------------:' + t.get_start_date() + ';enddate=' + t.get_end_date())
        # print(t.print_data_range())
        g.set_data(t, t.get_start_date(), t.get_end_date(), chartType)
        self.graph = g
        g.graph_plot()

    def send_email(self, name, subject, fromEmail, msg):
        # print("In model sending email: " + name + subject + fromEmail + msg)
        self.email.send_email(name, subject, fromEmail, msg)
# if __name__ == '__main__':

#     m = Model()
#     g = graphData.GraphData()
#     t = ticker.Ticker('AAPL')
#     t.import_data_range('2021-01-01', '2021-12-31')
#     # data = m.get_db().find_data_from_db('AAPL')
#     # df = pd.DataFrame(list(data))
#     # t.add_data_from_database(df)
#     # t.set_data_range('2021-01-01', '2021-12-31')
#     g.set_data(t, t.get_start_date(), t.get_end_date(), 'line')
#     g.graph_plot()

