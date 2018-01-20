import config
from momentum import get_squeeze_bar
# Define Custom imports
from BinanceAPI import *
from collections import namedtuple
import datetime

# Define Custom import vars
client = BinanceAPI(config.api_key, config.api_secret)


class Kline(object):
    def __init__(self, symbol, kline_api_response):
        self.symbol = symbol

        self.open_time = int(kline_api_response[0])
        self.open = float(kline_api_response[1])
        self.high = float(kline_api_response[2])
        self.low = float(kline_api_response[3])
        self.close = float(kline_api_response[4])
        self.volume = float(kline_api_response[5])
        self.close_time = int(kline_api_response[6])
        self.quote_asset_volume = float(kline_api_response[7])
        self.no_of_trades = int(kline_api_response[8])
        self.taker_buy_base_asset_volume = float(kline_api_response[9])
        self.taker_buy_quote_asset_volume = float(kline_api_response[10])

    def __str__(self):
        return '{symbol}\n\topened at {open_time} with {open}\n\tclosed at {close_time} with {close}\n\thigh of {high} and low at {low}'.format(
                symbol=self.symbol,
                open_time=datetime.datetime.fromtimestamp(self.open_time/1000),
                open=self.open,
                close_time=datetime.datetime.fromtimestamp(self.close_time/1000),
                close=self.close,
                high=self.high,
                low=self.low,
            )

def main():
    kline_set = []

    for kline in client.get_kline('BCDBTC', '1m'):
        kline_set.append(Kline('BCDBTC', kline[:11]))

    opens = [kline.open for kline in kline_set]
    closes = [kline.close for kline in kline_set]
    highs = [kline.high for kline in kline_set]
    lows = [kline.low for kline in kline_set]

    bcolor, scolor = get_squeeze_bar(opens, closes, highs, lows)
    print bcolor, scolor

if __name__ == "__main__":
    main()