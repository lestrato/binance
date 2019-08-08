from collections import namedtuple
import datetime
from decimal import Decimal


class Kline(object):
    BUY_CODE = 1
    SELL_CODE = 0
    HOLD_CODE = -1

    def __init__(self, symbol, kline_api_response):
        self.symbol = symbol

        self.open_time = int(kline_api_response[0])
        self.open = Decimal(kline_api_response[1])
        self.high = Decimal(kline_api_response[2])
        self.low = Decimal(kline_api_response[3])
        self.close = Decimal(kline_api_response[4])
        self.volume = Decimal(kline_api_response[5])
        self.close_time = int(kline_api_response[6])
        self.quote_asset_volume = float(kline_api_response[7])
        self.no_of_trades = int(kline_api_response[8])
        self.taker_buy_base_asset_volume = float(kline_api_response[9])
        self.taker_buy_quote_asset_volume = float(kline_api_response[10])
 
        self.wavetrend_wt1 = None
        self.wavetrend_wt2 = None
        self.has_crossed = None

        self.godmode_wt1 = None
        self.godmode_wt2 = None
        self.extended = None

    def __str__(self):
        return '\n{symbol} : {open_time} to {close_time}\n\
                Open: {open}\n\
                Close: {close}\n\
                High: {high}\n\
                Low: {low}'.format(
                symbol=self.symbol,
                open_time=self.open_time_dt,
                close_time=self.close_time_dt,
                open=self.open,
                close=self.close,
                high=self.high,
                low=self.low,
            )

    @property
    def wavetrend_stats(self):
        return '\t\tWavetrend: wt1 of {wt1} and wt2 of {wt2} with {cross}'.format(
            wt1=round(self.wavetrend_wt1, 3),
            wt2=round(self.wavetrend_wt2, 3),
            cross='a crossover' if self.has_crossed else 'no crossover'
        )

    @property
    def godlike_stats(self):
        return '\t\tGodlike: wt1 of {wt1} and wt2 of {wt2} with {extended}'.format(
            wt1=round(self.godmode_wt1, 3),
            wt2=round(self.godmode_wt2, 3),
            extended='extension' if self.extended else 'no extension'
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

        if not self.has_crossed or not self.extended:
            return Kline.HOLD_CODE

        if (self.wavetrend_wt1 > self.wavetrend_wt2) and self.wavetrend_wt2 < -53 and self.extended < 25:
            return Kline.BUY_CODE

        elif (self.wavetrend_wt2 > self.wavetrend_wt1) and self.wavetrend_wt1 > 53 and self.extended > 75:
            return Kline.SELL_CODE

        else:
            return Kline.HOLD_CODE