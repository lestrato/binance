// Tradingview.com
// @author LazyBear, xSilas, Ni6HTH4wK, SNOW_CITY
// Drop a line if you use or modify this code. - SNOW_CITY Remove BTCe added BITSTAMP, Changed default varibles USE ON 1m, 5M, 15M charts

n1 = input(17, "Channel Length")
n2 = input(6, "Average Length")
n3 = input(4, "Short length")
multi = input(type=bool, defval=false, title="Multi-exchange?")
src0 = hlc3 

tci(src) => ema((src - ema(src, n1)) / (0.025 * ema(abs(src - ema(src, n1)), n1)), n2)+50
mf(src) => rsi(sum(volume * (change(src) <= 0 ? 0 : src), n3), sum(volume * (change(src) >= 0 ? 0 : src), n3))
willy(src) => 60 * (src - highest(src, n2)) / (highest(src, n2) - lowest(src, n2)) + 80
csi(src) => avg(rsi(src, n3),tsi(src0,n1,n2)*50+50)

godmode(src) => avg(tci(src),csi(src),mf(src),willy(src))
tradition(src) => avg(tci(src),mf(src),rsi(src, n3))

wt1 = tradition(src0)
wt2 = sma(wt1,6)

extended = wt2<20 ? wt2+5 : wt2>80 ? wt2-5 : na

plot(extended, title="Caution!", color=red, style=circles, linewidth=2)

hline(80)
hline(20)

