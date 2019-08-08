import config
from indicators import get_squeeze_bar, get_wavetrend_cross, get_godlike
# Define Custom imports
from BinanceAPI import *
from kline import Kline

from decimal import Decimal

from history_tester import history_tester

# Define Custom import vars
client = BinanceAPI(config.api_key, config.api_secret)

def attach_wavetrend(kline_set):

    opens = [Decimal(kline.open) for kline in kline_set]
    closes = [Decimal(kline.close) for kline in kline_set]
    highs = [Decimal(kline.high) for kline in kline_set]
    lows = [Decimal(kline.low) for kline in kline_set]

    wt1, wt2, cross_list = get_wavetrend_cross(opens, closes, highs, lows)
    for (kline, w1, w2, crossed) in zip(kline_set, wt1, wt2, cross_list):
        kline.wavetrend_wt1 = w1
        kline.wavetrend_wt2 = w2
        kline.has_crossed = crossed

def attach_godlike(kline_set):

    opens = [Decimal(kline.open) for kline in kline_set]
    closes = [Decimal(kline.close) for kline in kline_set]
    highs = [Decimal(kline.high) for kline in kline_set]
    lows = [Decimal(kline.low) for kline in kline_set]
    volumes = [Decimal(kline.volume) for kline in kline_set]

    wt1, wt2 = get_godlike(opens, closes, highs, lows, volumes)
    for (kline, w1, w2) in zip(kline_set, wt1, wt2):
        kline.godmode_wt1 = w1
        kline.godmode_wt2 = w2
        kline.extended = w2 + 5 if w2 < 20 else w2 - 5 if w2 > 80 else None


def tester(coin):
    kline_set = []
    for kline in client.get_kline(coin, '3m'):
        kline_set.append(Kline(coin, kline[:11]))

    attach_wavetrend(kline_set)
    attach_godlike(kline_set)

    return history_tester(kline_set)



if __name__ == "__main__":
    coins = ['XLMBTC', 'OSTBTC', 'ADABTC', 'NEOBTC', 'ENJBTC', 'FUNBTC', 'QTUMBTC', 'ICXBTC', 'XRPBTC']
    # coins = ['BTCUSDT']
    total_trade_count = Decimal(0)
    total_net_earnings = Decimal(0)
    total_percent_made = Decimal(0)
    for coin in coins:
        trade_count, net_earnings, percent_made = tester(coin)
        total_trade_count += trade_count
        total_net_earnings += net_earnings
        total_percent_made += percent_made
        print '========================'

    print 'TOTAL TRADE COUNT: {trade_count}'.format(trade_count=total_trade_count)
    print 'TOTAL NET EARNINGS: ${net_earnings}'.format(net_earnings=total_net_earnings)
    print 'TOTAL PERCENT MADE: {percent_made}%'.format(percent_made=total_percent_made)
    print 'AVERAGE NET EARNINGS: ${average_earnings}'.format(average_earnings=total_net_earnings/total_trade_count)
    print 'AVERAGE PERCENT MADE: {average_percent_made}%'.format(average_percent_made=round(total_percent_made/total_trade_count, 2))