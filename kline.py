from collections import namedtuple
import datetime

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
        return '{symbol}\n\topened at {open_time} with {open}\n\t{has_closed}\n\thigh of {high} and low at {low}'.format(
                symbol=self.symbol,
                open_time=datetime.datetime.fromtimestamp(self.open_time/1000),
                open=self.open,
                has_closed='closed at {close_time} with {close}'.format(
                    close_time=datetime.datetime.fromtimestamp(self.close_time/1000),
                    close=self.close,
                ) if self.has_closed else 'has not closed yet',
                high=self.high,
                low=self.low,
            )

    @property
    def has_closed(self):
        return datetime.datetime.fromtimestamp(self.close_time/1000) < datetime.datetime.now() 
