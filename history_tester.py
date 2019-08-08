from kline import Kline
from decimal import Decimal

def history_tester(kline_set):
    # for testing purposes
    starting_wallet = Decimal(55.00) # usd of course
    transaction_amount = Decimal(25.00)
    wallet = starting_wallet
    # coins_holding = 0.0
    transaction_fee = Decimal(0.001) # 0.1 / 100
    trade_count = Decimal(0)
    total_transaction_costs = Decimal(0.00)
    optimal_profit = Decimal(1.03) # percent
    bought_at = {}
    wallet_history = []

    print 'TRADES for {coin}:'.format(coin=kline_set[0].symbol)

    for k in range(len(kline_set)):
        last_kline = kline_set[k - 1]
        current_kline = kline_set[k]

        # find if any of the buy orders rose above 0.8% of what it is now
        risen = [bought_price for bought_price in bought_at.keys() if last_kline.action == Kline.SELL_CODE or ((last_kline.wavetrend_wt2 > last_kline.wavetrend_wt1) and bought_price * optimal_profit < last_kline.open)] #
        # find if any of the buy orders fell below 80% of what it is now
        fallen = []

        if last_kline.action == Kline.BUY_CODE and len(bought_at) == 0:
            coins_bought = transaction_amount / current_kline.open
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

                del bought_at[buy_price]
                trade_count += 1
                wallet_history.append(wallet)

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

    trade_count /= 2
    print '-------------'
    print 'STATISTICS for {coin}:'.format(coin=kline_set[0].symbol)
    print 'First trade time: {open_time}'.format(open_time=kline_set[0].open_time_dt)
    print 'Last trade time: {close_time}'.format(close_time=kline_set[-1].close_time_dt)
    print 'Total flips made: {trade_count}'.format(trade_count=trade_count)
    print 'Total transaction cost: ${transaction_cost}'.format(transaction_cost=round(total_transaction_costs, 2))

    print 'Starting wallet: ${starting_wallet}'.format(starting_wallet=round(starting_wallet, 2))
    print 'End wallet: ${wallet}'.format(wallet=round(wallet, 2))
    print 'Net total: ${net_earnings} ({percent_made}%)'.format(
        net_earnings=round(wallet - starting_wallet, 2),
        percent_made=round((wallet / starting_wallet - 1) * 100, 2)
    )

    return trade_count, wallet - starting_wallet, (wallet / starting_wallet - 1) * 100
