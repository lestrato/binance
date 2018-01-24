# -*- coding: UTF-8 -*-
# @lestrato

# Define Python imports
import os
import sys
import time
import config
import argparse
import threading
import sqlite3
import config
import time
import datetime

# Define Custom imports
from balance import Binance
from BinanceAPI import *
from kline import Kline
from indicators import get_wavetrend_cross


# Define Custom import vars
binance = Binance()
client = BinanceAPI(config.api_key, config.api_secret)
conn = sqlite3.connect('orders.db')

# Set parser
parser = argparse.ArgumentParser()
parser.add_argument("--calibrate", dest="calibrate", action="store_true", help="Waits until the end of the minute to make orders")
parser.add_argument("--no-calibrate", dest="calibrate", action="store_false", help="Waits until the end of the minute to make orders")
parser.set_defaults(calibrate=True)

option = parser.parse_args()

# Define parser vars
CALIBRATE = option.calibrate

# Define static vars
TRANSACTION_FEE = 0.0005 # percent
MINIMUM_BUY_IN = 0.0022 # satoshis
OVERSOLD_LEVEL = -60

class Transaction:
    def __init__(self, buy_price, buy_time, amount, sell_price=None, sell_time=None):
        self.buy_price = buy_price
        self.buy_time = buy_time
        self.sell_price = sell_price
        self.sell_time = sell_time
        self.amount = amount

class TransactionHistory:
    def __init__(self, coin):
        self.history = []
        self.wallet = 0.005
        self.coin = coin

    @property
    def history_not_sold(self):
        return [transaction for transaction in self.history if transaction.sell_time == None]

    def trader(self):

        threading.Timer(interval=60.0, function=self.trader).start()

        kline_set = []

        for kline in client.get_kline(self.coin, '1m'):
            kline_set.append(Kline(self.coin, kline[:11]))

        opens = [kline.open for kline in kline_set]
        closes = [kline.close for kline in kline_set]
        highs = [kline.high for kline in kline_set]
        lows = [kline.low for kline in kline_set]

        wt1, wt2, cross_list = get_wavetrend_cross(opens, closes, highs, lows)
        for (kline, w1, w2, crossed) in zip(kline_set, wt1, wt2, cross_list):
            kline.wt1 = w1
            kline.wt2 = w2
            kline.has_crossed = crossed

        last_kline = kline_set[-2]
        current_kline = kline_set[-1]

        # find if any of the buy orders rose above 0.8% of what it is now
        risen = [transaction for transaction in self.history_not_sold if (transaction.buy_price * 1.03 < current_kline.open)]
        # find if any of the buy orders fell below 80% of what it is now
        fallen = [transaction for transaction in self.history_not_sold if (transaction.buy_price * 0.920 > current_kline.open)]

        if last_kline.action == Kline.BUY_CODE and last_kline.wt1 < OVERSOLD_LEVEL:
            coins_bought = (MINIMUM_BUY_IN // current_kline.open) + 1
            purchase = coins_bought * current_kline.open

            print ('Trying to buy {coins_bought} {coin} for {bought_at}'.format(coins_bought=coins_bought, coin=self.coin, )bought_at=current_kline.open)

            # check if we have enough for this purchase
            if float(binance.balances['BTC']) < purchase:
                print ("You don't have enough BTC to make this purchase ({btc_wallet} remaining)".format(btc_wallet=binance.balances['BTC']))
                return

            if self.wallet < purchase:
                print ("You've capped out this {coin} and have {wallet} left in-wallet".format(coin=self.coin, wallet=self.wallet))
                return

            self.wallet -= purchase
            self.wallet -= TRANSACTION_FEE * purchase

            self.history.append(Transaction(buy_time=current_kline.open_time, buy_price=current_kline.open, amount=coins_bought))
            print ('Bought {coins_bought} {coin} for {bought_at} at {trade_time}'.format(coins_bought=coins_bought, coin=self.coin, bought_at=current_kline.open, trade_time=current_kline.open_time_dt))
            print ('You have {wallet} left in your {coin} wallet'.format(wallet=self.wallet, coin=self.coin))
            print ('----------')

        if last_kline.action == Kline.SELL_CODE and (risen or fallen):
            for transaction in risen + fallen:
                sale = transaction.amount * current_kline.open

                print ('Trying to sell {coins_holding} {coin} for {sold_at}'.format(coins_holding=transaction.amount, coin=)self.coin, sold_at=current_kline.open)

                if sale < MINIMUM_BUY_IN:
                    print ("Couldn't sell the coins, under transaction minimum.")
                    return

                self.wallet += sale
                self.wallet -= TRANSACTION_FEE * sale

                transaction.sell_price = current_kline.open
                transaction.sell_time = current_kline.open_time

                print ('Sold {coins_holding} {coin} for {sold_at} at {trade_time}'.format(coins_holding=transaction.amount, )coin=self.coin, sold_at=current_kline.open, trade_time=current_kline.open_time_dt)

                print ('You have {wallet} left in your {coin} wallet'.format(wallet=self.wallet, coin=self.coin))
                print ('----------')

        # we don't know if the coin needs an int buy in total, or can just use a float.

def main():
    symbols = ['ADABTC', 'TRXBTC', 'XVGBTC',  'ICXBTC']

    print ("@lestrato, 2017")
    print ("Auto Trading for Binance.com.")
    print ("CTRL-Z to exit at any time")
    print ("")
    print ("We're looking to trade: {symbols}".format(symbols=symbols))

    if CALIBRATE:
        print ("Synchronizing... please wait {seconds} seconds.".format(seconds=65 - datetime.datetime.now().second))
        # only start running the threads at the beginning of the 60 second period (i.e. start of minute)
        time.sleep(70 - datetime.datetime.now().second)
    else:
        print ("Skipping calibration.")

    # start new threads for each of these coins
    for symbol in symbols:
        print ("Starting the trader on {symbol}".format(symbol=symbol))
        transaction_history = TransactionHistory(symbol)
        traderAction = threading.Thread(target=transaction_history.trader)
        traderAction.start()

    print ("")
           

if __name__ == "__main__":
    main()