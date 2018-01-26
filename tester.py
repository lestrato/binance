import config
from momentum import get_squeeze_bar, get_wavetrend_cross
# Define Custom imports
from BinanceAPI import *
from kline import Kline

# Define Custom import vars
client = BinanceAPI(config.api_key, config.api_secret)
coin = 'NEOBTC'


def main(coin):
    kline_set = []

    for kline in client.get_kline(coin, '3m'):
        kline_set.append(Kline(coin, kline[:11]))

    opens = [kline.open for kline in kline_set]
    closes = [kline.close for kline in kline_set]
    highs = [kline.high for kline in kline_set]
    lows = [kline.low for kline in kline_set]

    wt1, wt2, cross_list = get_wavetrend_cross(opens, closes, highs, lows)
    for (kline, w1, w2, crossed) in zip(kline_set, wt1, wt2, cross_list):
        kline.wt1 = w1
        kline.wt2 = w2
        kline.has_crossed = crossed


    # for testing purposes
    obLevel1 = 40 # overbought level 1
    obLevel2 = 33 # overbought level 2
    osLevel1 = -40 # oversold level 1
    osLevel2 = -33# oversold level 2

    starting_wallet = 55.00 # usd of course
    transaction_amount = 25.00
    wallet = starting_wallet
    # coins_holding = 0.0
    transaction_fee = 0.001 # 0.1 / 100
    trade_count = 0
    total_transaction_costs = 0.00
    bought_at = {}
    wallet_history = []

    print 'TRADES for {coin}:'.format(coin=coin)

    remove_from_wallet = False
    for k in range(len(kline_set)):
        last_kline = kline_set[k - 1]
        current_kline = kline_set[k]

        # find if any of the buy orders rose above 0.8% of what it is now
        risen = [bought_price for bought_price in bought_at.keys() if last_kline.action == Kline.SELL_CODE and last_kline.wt1 > obLevel2]
        # find if any of the buy orders fell below 80% of what it is now
        fallen = []

        if last_kline.action == Kline.BUY_CODE and last_kline.wt1 < osLevel1 and current_kline.wt1 > osLevel1 and wallet > transaction_amount and len(bought_at) == 0:
            coins_bought = transaction_amount // current_kline.open
            transaction = coins_bought * current_kline.open
            wallet -= transaction
            wallet -= transaction_fee * transaction
            total_transaction_costs += transaction_fee * transaction
            # coins_holding += coins_bought
            trade_count += 1
            bought_at[current_kline.open] = coins_bought
            print 'Bought {coins_bought} for {bought_at} at {trade_time}'.format(coins_bought=coins_bought, bought_at=current_kline.open, trade_time=current_kline.open_time_dt)
            wallet_history.append(wallet)

        if risen or fallen:
            for buy_price in risen + fallen:
                amount_sold = bought_at[buy_price]
                print 'Sold {coins_holding} at {sold_at} at {trade_time}'.format(coins_holding=amount_sold, sold_at=current_kline.open, trade_time=current_kline.open_time_dt)
                transaction = amount_sold * current_kline.open
                wallet += transaction
                wallet -= transaction_fee * transaction
                total_transaction_costs += transaction_fee * transaction

                remove_from_wallet = bought_at[buy_price] > (current_kline.open * 1.001)

                del bought_at[buy_price]
                trade_count += 1
                wallet_history.append(wallet)

            # if remove_from_wallet: break

    if len(bought_at):
        print '------ END OF DAY DUMPS ------'

    for buy_price in bought_at.keys():
        amount_sold = bought_at[buy_price]
        print 'Sold {coins_holding} at {sold_at} at {trade_time}'.format(coins_holding=amount_sold, sold_at=current_kline.open, trade_time=current_kline.open_time_dt)
        transaction = amount_sold * current_kline.open
        wallet += transaction
        wallet -= transaction_fee * transaction
        total_transaction_costs += transaction_fee * transaction
        del bought_at[buy_price]
        trade_count += 1
        wallet_history.append(wallet)

    # if coins_holding != 0.0:
    #     wallet = wallet_history[-2] if len(wallet_history) > 1 else starting_wallet

    # if coins_holding != 0.0:
    #     print 'Sold {coins_holding} at {sold_at}'.format(coins_holding=coins_holding, sold_at=current_kline.open)
    #     transaction = coins_holding * current_kline.open
    #     wallet += transaction
    #     wallet -= transaction_fee * transaction
    #     total_transaction_costs += transaction_fee * transaction
    #     coins_holding = 0.0
    #     trade_count += 1
    #     wallet_history.append(wallet)

    print '-------------'
    print 'STATISTICS for {coin}:'.format(coin=coin)
    print 'First trade time: {open_time}'.format(open_time=kline_set[0].open_time_dt)
    print 'Last trade time: {close_time}'.format(close_time=kline_set[-1].close_time_dt)
    print 'Total trades made: {trade_count}'.format(trade_count=trade_count)
    print 'Total transaction cost: ${transaction_cost}'.format(transaction_cost=round(total_transaction_costs, 2))

    print 'Starting wallet: ${starting_wallet}'.format(starting_wallet=round(starting_wallet, 2))
    print 'End wallet: ${wallet}'.format(wallet=round(wallet, 2))
    print 'Net total: ${net_earnings} ({percent_made}%)'.format(
        net_earnings=round(wallet - starting_wallet, 2),
        percent_made=round((wallet / starting_wallet - 1) * 100, 2)
    )

    return trade_count, round(wallet - starting_wallet, 2), round((wallet / starting_wallet - 1) * 100, 2)

if __name__ == "__main__":
    total_trade_count = 0
    total_net_earnings = 0
    total_percent_made = 0
    for coin in ['XLMBTC', 'OSTBTC', 'ADABTC', 'NEOBTC', 'ENJBTC', 'FUNBTC', 'QTUMBTC', 'ICXBTC']:
        trade_count, net_earnings, percent_made = main(coin)
        total_trade_count += trade_count
        total_net_earnings += net_earnings
        total_percent_made += percent_made
        print '========================'

    print 'TOTAL TRADE COUNT: {trade_count}'.format(trade_count=total_trade_count)
    print 'TOTAL NET EARNINGS: ${net_earnings}'.format(net_earnings=total_net_earnings)
    print 'TOTAL PERCENT MADE: {percent_made}%'.format(percent_made=total_percent_made)
    print 'AVERAGE NET EARNINGS: ${average_earnings}'.format(average_earnings=total_net_earnings/total_trade_count)
    print 'AVERAGE PERCENT MADE: {average_percent_made}%'.format(average_percent_made=round(total_percent_made/total_trade_count, 2))