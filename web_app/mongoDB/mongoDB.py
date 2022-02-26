
import pymongo
import certifi
import os
import sys
import json
from pymongo import MongoClient

sys.path.insert(1,os.getcwd() + '/web_app')
from algo_model import *

class Table:
    Data = 'data'
    Ticker = 'ticker'

class MongoDB:

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        self.collection = None

    def connect_to_db(self):
        # f = open(os.getcwd() + '/web_app/config/config.json')
        # jsonData = json.load(f)
        # connectionString = jsonData['MONGODB_CONNECTION']
        connectionString = os.environ.get('MONGODB_CONNECTION')
        cluster = MongoClient(connectionString, tlsCAFile=certifi.where())

        db = cluster['algoDB']
        self.collectionTicker = db[Table.Ticker]
        self.collectionData = db[Table.Data]

    def insert_to_db(self, ticker):
        tickerName = ticker.get_ticker_name()
        df = ticker.get_data()
        for data in df.to_dict('records'):
            data['ticker'] = tickerName
            self.collectionData.insert_one(data)
        self.collectionTicker.insert_one({'ticker': tickerName})

    def get_all_ticker_from_db(self):
        dict = self.collectionTicker.find()
        ticker = []
        for v in dict:
            ticker.append(v['ticker'])
        return ticker

    def find_ticker_from_db(self, ticker):
        cursor = self.collectionTicker.find({'ticker': ticker})
        return len(list(cursor)) > 0

    def find_data_from_db(self, ticker):
        return self.collectionData.find({'ticker': ticker})
    
    def delete_records(self, ticker):
        self.collectionTicker.delete_many({'ticker': ticker})
        self.collectionData.delete_many({'ticker': ticker})
    
    def delete_all(self):
        self.collectionTicker.delete_many({})
        self.collectionData.delete_many({})


# if __name__ == '__main__':
#     m = MongoDB()
#     m.connect_to_db()
#     m.delete_all()
    # t = Ticker.Ticker('AAPL')
    # t.import_data_range('2021-06-01','2021-06-30')
    # # t.print_data_range()
    # m.insert_to_db(t)
    # print(m.find_ticker_from_db())