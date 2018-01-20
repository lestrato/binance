import config
from momentum import get_squeeze_bar, get_wavetrend_cross
# Define Custom imports
from BinanceAPI import *
from kline import Kline

# Define Custom import vars
client = BinanceAPI(config.api_key, config.api_secret)
coin = 'NEOBTC'


def main():
    kline_set = []

    for kline in client.get_kline(coin, '1m'):
        kline_set.append(Kline(coin, kline[:11]))

    opens = [kline.open for kline in kline_set]
    closes = [kline.close for kline in kline_set]
    highs = [kline.high for kline in kline_set]
    lows = [kline.low for kline in kline_set]

    wt1, wt2, cross_list = get_wavetrend_cross(opens, closes, highs, lows)
    for (kline, w1, w2, crossed) in zip(kline_set, wt1, wt2, cross_list):
        print kline
        print '>>> {0}, {1}, {2}'.format(w1, w2, crossed)

if __name__ == "__main__":
    main()