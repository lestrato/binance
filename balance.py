#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-
# @yasinkuyu

from BinanceAPI import *

import config

class Binance:

    def __init__(self):
        self.client = BinanceAPI(config.api_key, config.api_secret)

    @property
    def balances(self):
        balances = self.client.get_account()
        return { balance['asset']: balance['free'] for balance in balances['balances'] if float(balance["locked"]) > 0 or float(balance["free"]) > 0 } 

    def orders(self, symbol, limit):
        orders = self.client.get_open_orders(symbol, limit)

        print orders

    def tickers(self):
       return self.client.get_all_tickers()

    def server_time(self):
       return self.client.get_server_time()

    def openorders(self):
       return self.client.get_open_orders()
