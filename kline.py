from collections import namedtuple
import datetime


class Kline(object):
    BUY_CODE = 1
    SELL_CODE = 0
    HOLD_CODE = -1

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
 
        self.wt1 = None
        self.wt2 = None
        self.has_crossed = None

    def __str__(self):
        return '{symbol}\n\
                opened at {open_time} with {open}\n\
                {has_closed}\n\
                high of {high} and low at {low}\n\
                wt1 of {wt1} and wt2 of {wt2} with {cross}\n'.format(
                symbol=self.symbol,
                open_time=self.open_time_dt,
                open=self.open,
                has_closed='closed at {close_time} with {close}'.format(
                    close_time=self.close_time_dt,
                    close=self.close,
                ) if self.has_closed else 'has not closed yet',
                high=self.high,
                low=self.low,
                wt1=round(self.wt1, 3),
                wt2=round(self.wt2, 3),
                cross='a crossover' if self.has_crossed else 'no crossover',
            )

    @property
    def has_closed(self):
        return self.close_time_dt < datetime.datetime.now() 

    @property
    def open_time_dt(self):
        return datetime.datetime.fromtimestamp(self.open_time/1000)

    @property
    def close_time_dt(self):
        return datetime.datetime.fromtimestamp(self.close_time/1000)

    @property
    def action(self):
        if not self.has_crossed:
            return Kline.HOLD_CODE

        if self.wt1 > self.wt2:
            return Kline.BUY_CODE

        else:
            return Kline.SELL_CODE