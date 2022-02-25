#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
import json
from .ticker import Ticker
from bs4 import BeautifulSoup


# class to import the s&p 500 ticker from the wikipedia. 
# request to graph the ticker symbol from the wikipedia, the result can feed into the UI
class Data():

    def __init__(self) -> None:
        self.__tickerDict = {}
        f = open(os.getcwd() + '/web_app/config/config.json')
        # f = open(os.getcwd() + '/web_app/algo_model/config/config.json')
        jsonData = json.load(f)
        self.wikiPath = jsonData['WIKI_PATH']
    
    # this is the function to read data from the wikipedia.
    def read_wiki(self):

        try:
            r = requests.get(self.wikiPath).text
            soup = BeautifulSoup(r)
            s = soup.find('table').find_all('a', {'external text'})

            for i in range(len(s)):
                if len(self.__tickerDict) > 500:
                    break
                if s[i].contents != ['reports']:
                    ticker = s[i].contents[0]
                    t = Ticker(ticker)
                    self.__tickerDict[ticker] = t
        except:
            raise "read wiki error!"

    # function to return all the tickers symbol
    def get_all_ticker(self):
        tickerName = []
        for i in self.__tickerDict.keys():
            tickerName.append(self.__tickerDict[i].get_ticker_name())
        return tickerName

    def check_if_ticker_exists(self, ticker):
        return ticker in self.__tickerDict

# if __name__ == '__main__':
    # d = Data()
    # d.read_wiki()
    # d.get_all_ticker()
