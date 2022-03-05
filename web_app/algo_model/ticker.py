#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import pandas
import requests
import os
from datetime import datetime, timedelta

# this is the ticker class
# ticker class contain the ticker name, start date, end date as the data within this period
# the ticker can be empty when initizalize
# this class will grap the data from the polygon web API
# this a free account, so the download max is 5/ minutes, error will raise if reach the limitation.
class Ticker:

    def __init__(self, ticker) -> None:
        # f = open(os.getcwd() + '/web_app/config/config.json')
        # f = open(os.getcwd() + '/web_app/algo_model/config/config.json')
        # jsonData = json.load(f)
        # self.configKey = jsonData['POLYGON_KEY']
        self.configKey = os.environ.get('POLYGON_KEY')
        self.__name = ticker
        self.__data = None
        self.__startDate = '1990-01-01'
        self.__endDate = '1990-01-01'

    # this is the import data function to import the data from the polygon API
    def import_data_range(self, startDate, endDate):
        format = "%Y-%m-%d"
        try:
            data = requests.get('https://api.polygon.io/v2/aggs/ticker/' + self.__name 
                + '/range/1/day/' + startDate + '/' + endDate + '?adjusted=true&sort=asc&limit=1000&apiKey=' + self.configKey).json()
            datetime.strptime(startDate, format)
            datetime.strptime(endDate, format)
            # print('https://api.polygon.io/v2/aggs/ticker/' + self.__name 
            #     + '/range/1/day/' + startDate + '/' + endDate + '?adjusted=true&sort=asc&limit=120&apiKey=' + self.configKey)
            # format = "%Y-%m-%d"
            yrsDiff = (datetime.strptime(endDate, format) - datetime.strptime(startDate, format)).total_seconds() // 31536000
            if yrsDiff > 2:
                raise "Invalid data range, can't load data more than 2 years."
            # f = open(os.getcwd() + '/model/data/AAPL.json')
            # data = json.load(data)
            # print(data['results'])
            df = pandas.DataFrame(data['results'])
            df = df[['t','o','h','l','c','v','vw','n']]
            df.rename(columns={'t': 'Date','o': 'Open','h': 'High','l': 'Low','c': 'Close','v': 'Volume'}, inplace=True)
            df['Date'] = pandas.to_datetime(df['Date'], unit='ms')
            df.index = pandas.DatetimeIndex(df['Date'])
            self.__startDate = startDate
            self.__endDate = endDate
            self.__data = df
        except ValueError: 
            raise "time data 'time' does not match format '%Y-%m-%d"
        except:
            raise "Import data fail error!"

    # reduce or increase the data size, this will base on the user request.
    # after the increase or reduce the size, the meneory will storage the newest use data into the ticker class
    def set_data_range(self, startDate, endDate):
        format = "%Y-%m-%d"
        # print('set Date Range---------------')
        if datetime.strptime(self.__startDate, format) > datetime.strptime(startDate, format) or datetime.strptime(self.__endDate, format) < datetime.strptime(endDate, format):
            # print('set Date Range---------------1')
            self.import_data_range(startDate, endDate)
        else:
            # print('set Date Range---------------2')
            mask = (self.__data['Date'] >= startDate) & (self.__data['Date'] <= datetime.strptime(endDate, format) + timedelta(1))
            self.__startDate = startDate
            self.__endDate = endDate
            self.__data = self.__data.loc[mask]

    # this class is for testing
    # def add_data(self, startDate, endDate, *args):
    #     format = "%m-%d-%Y"
    #     data = []
    #     self.__startDate = startDate
    #     self.__endDate = endDate
    #     for date, val in args:
    #         data.append([datetime.strptime(date, format), val])
        
    #     self.__data = pandas.DataFrame(data, columns = ['Date', 'Close'])

    def add_data_from_database(self, df):
        format = "%Y-%m-%d"
        # df.drop('ticker', axis=1, inplace=True)
        df.sort_values(by=['Date'])
        self.__startDate = df['Date'].min().strftime(format)
        self.__endDate = df['Date'].max().strftime(format)
        df.index = pandas.DatetimeIndex(df['Date'])
        self.__data = df

    def get_start_date(self):
        return self.__startDate
    
    def get_end_date(self):
        return self.__endDate

    def get_last_close_data(self):
        return self.__data.loc[self.__data.index[-1], "Close"]

    def get_data(self):
        return self.__data

    def check_if_has_data(self):
        return self.__name != None

    def get_ticker_name(self):
        return self.__name

    def print_data_range(self):
        print(self.__data.iloc[-1])


# if __name__ == '__main__':

    # t = Ticker('AAPL')
    # t.import_data_range('2021-01-01','2021-12-31')
    # t.print_data_range()
    # t.set_data_range('2021-06-15', '2021-06-28')
    # t.print_data_range()
