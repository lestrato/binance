from decimal import Decimal

def sma(x, y):
    '''
    https://www.tradingview.com/study-script-reference/#fun_sma
    the sum of moving averages
        @return the moving average, that is the sum of last y values of x, divided by y.
    '''
    return sum(x[-y:]) / y

def tr(high, low, last_close):
    '''
    https://www.tradingview.com/study-script-reference/#fun_tr
    true range. it is max(high - low, abs(high - last_close), abs(low - last_close))
        @return the true rangebased on the above formula
    '''
    return max(high - low, abs(high - last_close), abs(low - last_close))

def nz(series):
    ''' 
    https://www.tradingview.com/study-script-reference/#fun_nz
    NaN zeroes. replaces NaN values with zeros (or given value) in a series.
        @return the new series
    '''
    nz_series = []
    for val in series:
        try:
            val = float(val)
        except Exception as e:
            val = 0
        nz_series.append(val)

    return nz_series

def avg(*args):
    '''
    given a series, returns the average (mean)
        @return the average of a series
    '''
    return sum(args) / Decimal(len(args))


def hlc3(high, low, close):
    '''
    is a shortcut for (high+low+close)/3
        @returns float
    '''
    return (high+low+close)/Decimal(3)

def ema(source, length):
    '''
    the sma function returns the expnentially weighted moving average. 
    in ema, weighting factors decrease exponentially.
    it calculates by using a formula: EMA = alpha * x + (1-alpha) * EMA[1], where alpha = 2/(y+1)
        @source: a series of values to process
        @length: the number of bars
        @returns a series: exponential moving average of x with alpha = 2/(y+1)
    '''

    # the EMAtoday = EMAyesterday + alpha(price today - EMAyesterday)
    alpha = Decimal(2.0) / Decimal(length + 1)
    ema_return = []

    for c in range(len(source)):
        value = source[c]
        prev_ema = ema_return[c-1] if c > 0 else 0

        ema_today = alpha * value + (1 - alpha) * prev_ema
        ema_return.append(ema_today)

    return ema_return

def rma(source, length):
    '''
    moving average used in RSI. it is the exponentially weighted moving average with alpha = length - 1
        @source: a series of values to process
        @length: the number of bars
        @returns a series: expontential moving average of x with alpha = y - 1

    '''
    alpha = Decimal(1)/length
    rma_return = []

    for c in range(len(source)):
        value = source[c]
        prev_rma = rma_return[c-1] if c > 0 else 0

        rma_today = alpha * value + (Decimal(1) - alpha) * prev_rma

        rma_return.append(rma_today)

    return rma_return

def rsi(list1, list2):
    '''
    relative strength index: it is calculated based on rma's of upward and downward change of x
        @list1: a series of values to process
        @list2: a series of values to process, or an integer
        @returns relative strength index
    '''
    if type(list2) != list:
        upward = []
        downward = []

        for i in range(len(list1)):
            u = max(list1[i] - list1[i-1], 0) if i > 0 else 0
            d = max(list1[i-1] - list1[i], 0) if i > 0 else 0
            upward.append(u)
            downward.append(d)

        rma1 = rma(upward, list2)
        rma2 = rma(downward, list2)

    else:
        rma1 = list1
        rma2 = list2

    rs = list_division(rma1, rma2)

    return [Decimal(100) - (Decimal(100) / (Decimal(1) + r)) for r in rs]

def abs_list(source):
    '''
    runs abs on each value in the source
        @returns a series: absolute values of source param
    '''
    return [abs(value) for value in source]

def list_difference(list1, list2):
    '''
    subtracts list 2's values from list 1
        @returns the difference between list1 and list2
    '''
    return [v1 - v2 for (v1, v2) in zip(list1, list2)]

def multiply_list(source, multiplier):
    '''
    multiplies all values in the list by the multiplier
        @returns the list with the multiplied values
    '''
    return [value * multiplier for value in source]

def add_to_list(source, value):
    '''
    add the value to all elements in the list
        @returns the list with the added value to each element
    '''
    return [element + value for element in source]

def sum_list(source, length):
    '''
    sums the last y values of x
        @returns the sum of the last y values of x
    '''
    summed_list = []
    for v in range(1, len(source) + 1):
        last_y_values_sum = sum(source[v-length:v]) if v >= length else sum(source[0:v])
        summed_list.append(last_y_values_sum)
    return summed_list

def change(source, length=1):
    '''
    difference between current value and previous, x - x[y]
        @returns the difference between the current value and the previous
    '''
    return [source[s] - source[s-1] if s > 0 else 0 for s in range(len(source))]


def list_division(list1, list2):
    '''
    divides list2's values from list1's values
        @returns the list result of the divison(s)
    '''
    return [v1 / v2 if v2 != 0 else 0 for (v1, v2) in zip(list1, list2)]

def cross(list1, list2):
    '''
    returns True if the lists crossed since the last element
        @returns a series, with Boolean depending if a cross happened
    '''
    pairs = zip(list1, list2)
    cross_list = []
    for l in range(len(list1)):
        has_crossed = False
        if l > 0:
            last_pair = pairs[l-1]
            this_pair = pairs[l]
            if (last_pair[0] > last_pair[1] and this_pair[0] < this_pair[1]) or (last_pair[0] < last_pair[1] and this_pair[0] > this_pair[1]):
                has_crossed = True

        cross_list.append(has_crossed)
    return cross_list
