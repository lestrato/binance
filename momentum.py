
from statistics import stdev
from scipy.stats import linregress

def sma(x, y):
    '''
    https://www.tradingview.com/study-script-reference/#fun_sma
    the sum of moving averages
        @return the moving average, that is the sum of last y values of x, divided by y.
    '''
    sma_sum = 0.0
    for i in range(0, y - 1):
        sma_sum = sma_sum + x[i] / y

    return sma_sum

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

# global vars, could be arguments in the future
LENGTH = 20
MULT = 2.0
LENGTH_KC = 20
MULT_KC = 1.5

USE_TRUE_RANGE = True

# Calculate BB
source = close   # closing price
basis = sma(source, LENGTH)
dev = MULT_KC * stdev(source[-LENGTH:]) # standard deviation of x for y bars back.
upperBB = basis + dev
lowerBB = basis - dev

# Calculate KC
ma = sma(source, LENGTH_KC) 
_range = tr(high, low, close[1]) if USE_TRUE_RANGE else (high - low) # Current high price, Current low price.
rangema = sma(_range, LENGTH_KC)
upperKC = ma + rangema * MULT_KC
lowerKC = ma - rangema * MULT_KC

sqzOn  = (lowerBB > lowerKC) and (upperBB < upperKC)
sqzOff = (lowerBB < lowerKC) and (upperBB > upperKC)
noSqz  = (sqzOn == False) and (sqzOff == False)

# linreg: Linear regression curve. A line that best fits the prices specified over a user-defined time period. It is calculated using the least squares method. The result of this function is calculated using the formula: linreg = intercept + slope * (length - 1 - offset), where length is the y argument, offset is the z argument, intercept and slope are the values calculated with the least squares method on source series (x argument).

slope, intercept, r_value, p_value, std_err = linregress(
    source  -  avg(avg(max(high[-LENGTH_KC:]), min(low[-LENGTH_KC:])), sma(close,LENGTH_KC)), 
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




