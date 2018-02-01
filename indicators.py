
from statistics import stddev
from scipy.stats import linregress

from tradingview_methods import *

# global vars, could be arguments in the future
LENGTH = 20
MULT = 2.0
LENGTH_KC = 20
MULT_KC = 1.5

USE_TRUE_RANGE = True

def get_squeeze_bar(opens, closes, highs, lows):
    # Calculate BB
    source = closes   # closing prices
    basis = sma(source, LENGTH)
    dev = MULT_KC * stddev(source[-LENGTH:]) # standard deviation of x for y bars back.
    upperBB = basis + dev
    lowerBB = basis - dev


    last_close = closes[-1]
    current_high = highs[-1]
    current_low = lows[-1]


    # Calculate KC
    ma = sma(source, LENGTH_KC) 
    _range = [tr(high, low, last_close) for high, low in zip(highs, lows)] if USE_TRUE_RANGE else ([high - low for high, low in zip(highs, lows)]) # Current high price, Current low price.
    rangema = sma(_range, LENGTH_KC)
    upperKC = ma + rangema * MULT_KC
    lowerKC = ma - rangema * MULT_KC

    sqzOn  = (lowerBB > lowerKC) and (upperBB < upperKC)
    sqzOff = (lowerBB < lowerKC) and (upperBB > upperKC)
    noSqz  = (sqzOn == False) and (sqzOff == False)

    # linreg: Linear regression curve. A line that best fits the prices specified over a user-defined time period. It is calculated using the least squares method. The result of this function is calculated using the formula: linreg = intercept + slope * (length - 1 - offset), where length is the y argument, offset is the z argument, intercept and slope are the values calculated with the least squares method on source series (x argument).

    slope, intercept, r_value, p_value, std_err = linregress(
        source  -  avg(avg(max(highs[-LENGTH_KC:]), min(lows[-LENGTH_KC:])), sma(closes, LENGTH_KC)), 
                LENGTH_K)
    offset = 0
    linreg_val = intercept + slope * (LENGTH - 1 - offset)

    # lime is momentum up above x axis, green is momentum down above x axis 
    # red is momentum down below x axis, maroon is momentum up below x axis
    # get the bar-colour
    bcolor = None

    if linreg_val > 0:
        if linreg_val > nz(linreg_val[1]):
            bcolor = 'lime'
        else:
            bcolor = 'green'
    else:
        if linreg_val < nz(linreg_val[1]):
            bcolor = 'red'
        else:
            bcolor = 'maroon'

    # blue is no squeeze or the squeeze is on
    # orange is the squeeze is off
    if noSqz or sqzOn:
        scolor = 'blue'
    else: 
        scolor = 'orange'

    return bcolor, scolor


def get_wavetrend_cross(opens, closes, highs, lows):
    n1 = 10 # channel length
    n2 = 21 # average length

    ap = [hlc3(high, low, close) for (high, low, close) in zip(highs, lows, closes)]
    esa = ema(ap, n1)
    d = ema(abs_list(list_difference(ap, esa)), n1)
    ci = list_division(list_difference(ap, esa),  multiply_list(d, Decimal(0.015)))
    tci = ema(ci, n2)

    wt1 = tci
    wt2 = [sma(wt1[1:v+1], 4) for v in range(len(wt1))]

    cross_list = cross(wt1, wt2)

    return wt1, wt2, cross_list

def get_godlike(opens, closes, highs, lows, volumes):
    n1 = 14 # channel length
    n2 = 12 # average length
    n3 = 9 # short length
    srcs = [hlc3(high, low, close) for (high, low, close) in zip(highs, lows, closes)]
    volumes = [Decimal(volume) for volume in volumes]
    volume = volumes[-1]

    def tci(src):
        '''
        tci(src):
            ema(
                (src - ema(src, n1)) / (0.025 * ema(abs(src - ema(src, n1)), n1)),
                n2
            ) + 50

        >>> A = (src - ema(src, n1))
        >>> B = ema(abs(src - ema(src, n1)), n1)
        '''
        A = list_difference(src, ema(src, n1))
        B = ema([abs(value) for value in list_difference(src, ema(src, n1))], n1)
        return add_to_list(ema(list_division(A, multiply_list(B, Decimal(0.025))), n2), Decimal(50))

    def mf(src):
        '''
        mf(src):
            rsi(
                sum(
                    volume * (change(src) <= 0 ? 0 : src), 
                    n3), 
                sum(
                    volume * (change(src) >= 0 ? 0 : src),
                    n3
                )
            )
        '''
        change_list = change(src)

        neg_mult_change_list = [0 if change_list[i] <= 0 else volumes[i] * src[i] for i in range(len(src))]
        pos_mult_change_list = [0 if change_list[i] >= 0 else volumes[i] * src[i] for i in range(len(src))]

        return rsi(
            sum_list(neg_mult_change_list, n3), 
            sum_list(pos_mult_change_list, n3)
        )

    def tradition(src):
        return [avg(t, m, r) for (t, m, r) in zip(tci(src), mf(src), rsi(src, n3))]

    wt1 = tradition(srcs)
    wt2 = [sma(wt1[1:v+1], 6) for v in range(len(wt1))]

    return wt1, wt2
