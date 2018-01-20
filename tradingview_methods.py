
def sma(x, y):
    '''
    https://www.tradingview.com/study-script-reference/#fun_sma
    the sum of moving averages
        @return the moving average, that is the sum of last y values of x, divided by y.
    '''

    # print x
    # print y
    return sum(x[-y:]) / y

    # raise ValueError('stop')
    # return sma_sum

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
    return sum(args) / float(len(args))


def hlc3(high, low, close):
    '''
    is a shortcut for (high+low+close)/3
        @returns float
    '''
    return (high+low+close)/3.0

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
    alpha = 2.0 / (length + 1)
    ema_sum = 0.0

    ema_return = []

    for c in range(len(source)):
        value = source[c]
        prev_ema = ema_return[c-1] if c > 0 else 0

        ema_today = alpha * value + (1 - alpha) * prev_ema
        ema_return.append(ema_today)

    return ema_return
    
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

def list_division(list1, list2):
    '''
    divides list2's values from list1's values
        @returns the list result of the divison(s)
    '''
    return [v1 / v2 for (v1, v2) in zip(list1, list2)]

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
