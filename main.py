import json
import func_arb



btcturk_url = 'https://api.btcturk.com/api/v2/ticker'
ftx_url = 'https://ftx.com/api/markets'
coinbase_url = 'https://api.coinbase.com/v2/prices/usd/spot'
liverates_url='https://www.live-rates.com/rates'
alpha_rates_url='https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=TRY&apikey=AE966LKHL236KP1K'
kraken_url='https://api.kraken.com/0/public/AssetPairs?'
okx_url='https://www.okx.com/api/v5/market/tickers?instType=SWAP'
huobi_url='https://api.huobi.pro/market/tickers'
okcoin_url='https://www.okcoin.com/api/v3/otc/rfq/instruments'



#Initialise the tradable pairs between exchanges
def init_trade_pairs():


    # retrieve json objects from APIs
    btcturk_market = func_arb.get_ticker(btcturk_url)
    ftx_market = func_arb.get_ticker(ftx_url)
    coinbase_market = func_arb.get_ticker(coinbase_url)
    kraken_market=func_arb.get_ticker(kraken_url)
    okx_market=func_arb.get_ticker(okx_url)
    huobi_market=func_arb.get_ticker(huobi_url)
    okcoin_market=func_arb.get_ticker(okcoin_url)


    #Get the tickers for each pair in the exchnages
    btcturk_tickers= func_arb.get_btcturk(btcturk_market)
    ftx_tickers=func_arb.get_ftx(ftx_market)
    kraken_tickers=func_arb.get_kraken(kraken_market)
    coinbase_tickers=func_arb.get_coinbase(coinbase_market)
    okx_tickers=func_arb.get_okx(okx_market)
    huobi_tickers=func_arb.get_huobi(huobi_market)
    okcoin_tickers=func_arb.get_okcoin(okcoin_market)



    #Get the common tradable pairs between the exchanges
    trade_pairs_btcturk_ftx=func_arb.find_common_pairs(pair_1=ftx_tickers, pair_2=btcturk_tickers)
    trade_pairs_btcturk_coinbase=func_arb.find_common_pairs(pair_1=btcturk_tickers,pair_2=coinbase_tickers)
    trade_pairs_ftx_kraken=func_arb.find_common_pairs(pair_1=kraken_tickers,pair_2=ftx_tickers)
    trade_pairs_kraken_btcturk=func_arb.find_common_pairs(pair_1=kraken_tickers,pair_2=btcturk_tickers)
    trade_pairs_kraken_coinbase=func_arb.find_common_pairs(pair_1=kraken_tickers,pair_2=coinbase_tickers)
    trade_pairs_ftx_okx=func_arb.find_common_pairs(pair_1=ftx_tickers,pair_2=okx_tickers)
    trade_pairs_coinbase_okx=func_arb.find_common_pairs(pair_1=coinbase_tickers,pair_2=okx_tickers)
    trade_pairs_kraken_okx=func_arb.find_common_pairs(pair_1=kraken_tickers,pair_2=okx_tickers)
    trade_pairs_btcturk_okx=func_arb.find_common_pairs(pair_1=btcturk_tickers,pair_2=okx_tickers)
    trade_pairs_coinbase_okcoin=func_arb.find_common_pairs(pair_1=coinbase_tickers,pair_2=okcoin_tickers)
    trade_pairs_kraken_okcoin=func_arb.find_common_pairs(pair_1=kraken_tickers,pair_2=okcoin_tickers)
    trade_pairs_okx_okcoin=func_arb.find_common_pairs(pair_1=okx_tickers,pair_2=okcoin_tickers)
    trade_pairs_ftx_okcoin=func_arb.find_common_pairs(pair_1=ftx_tickers,pair_2=okcoin_tickers)
    trade_pairs_btcturk_okcoin=func_arb.find_common_pairs(pair_1=btcturk_tickers,pair_2=okcoin_tickers)
    trade_pairs_ftx_coinbase=func_arb.find_common_pairs(pair_1=ftx_tickers,pair_2=coinbase_tickers)
    trade_pairs_coinbase_huobi=func_arb.find_common_pairs(pair_1=coinbase_tickers,pair_2=huobi_tickers)
    trade_pairs_kraken_huobi=func_arb.find_common_pairs(pair_1=kraken_tickers,pair_2=huobi_tickers)
    trade_pairs_okx_huobi=func_arb.find_common_pairs(pair_1=okx_tickers,pair_2=huobi_tickers)
    trade_pairs_ftx_huobi=func_arb.find_common_pairs(pair_1=ftx_tickers,pair_2=huobi_tickers)
    trade_pairs_okcoin_huobi=func_arb.find_common_pairs(pair_1=okcoin_tickers,pair_2=huobi_tickers)
    trade_pairs_btcturk_huobi=func_arb.find_common_pairs(pair_1=btcturk_tickers,pair_2=huobi_tickers)


    #Save tradable pairs to file

    with open('trade_pairs_btcturk_ftx_dict.json', 'w') as ap:
        json.dump(trade_pairs_btcturk_ftx,ap)

    with open('trade_pairs_btcturk_coinbase_dict.json','w') as bp:
        json.dump(trade_pairs_btcturk_coinbase, bp)

    with open('trade_pairs_ftx_coinbase_dict.json','w') as cp:
        json.dump(trade_pairs_ftx_coinbase, cp)

    with open('trade_pairs_ftx_kraken_dict.json','w') as dp:
        json.dump(trade_pairs_ftx_kraken, dp)

    with open('trade_pairs_kraken_btcturk_dict.json', 'w') as ep:
        json.dump(trade_pairs_kraken_btcturk, ep)

    with open('trade_pairs_kraken_coinbase_dict.json', 'w') as fp:
        json.dump(trade_pairs_kraken_coinbase, fp)

    with open('trade_pairs_ftx_okx_dict.json', 'w') as gp:
        json.dump(trade_pairs_ftx_okx, gp)

    with open('trade_pairs_coinbase_okx_dict.json', 'w') as hp:
        json.dump(trade_pairs_coinbase_okx, hp)

    with open('trade_pairs_kraken_okx_dict.json', 'w') as ip:
        json.dump(trade_pairs_kraken_okx, ip)

    with open('trade_pairs_btcturk_okx_dict.json', 'w') as jp:
        json.dump(trade_pairs_btcturk_okx, jp)

    with open('trade_pairs_ftx_okcoin_dict.json', 'w') as kp:
        json.dump(trade_pairs_ftx_okcoin, kp)

    with open('trade_pairs_coinbase_okcoin_dict.json', 'w') as lp:
        json.dump(trade_pairs_coinbase_okcoin, lp)

    with open('trade_pairs_kraken_okcoin_dict.json', 'w') as mp:
        json.dump(trade_pairs_kraken_okcoin, mp)

    with open('trade_pairs_btcturk_okcoin_dict.json', 'w') as np:
        json.dump(trade_pairs_btcturk_okcoin, np)

    with open('trade_pairs_okx_okcoin_dict.json', 'w') as op:
        json.dump(trade_pairs_okx_okcoin, op)

    with open('trade_pairs_ftx_huobi_dict.json', 'w') as qp:
        json.dump(trade_pairs_ftx_huobi, qp)

    with open('trade_pairs_coinbase_huobi_dict.json', 'w') as rp:
        json.dump(trade_pairs_coinbase_huobi, rp)

    with open('trade_pairs_kraken_huobi_dict.json', 'w') as sp:
        json.dump(trade_pairs_kraken_huobi, sp)

    with open('trade_pairs_okx_huobi_dict.json', 'w') as up:
        json.dump(trade_pairs_okx_huobi, up)

    with open('trade_pairs_okcoin_huobi_dict.json', 'w') as up:
        json.dump(trade_pairs_okcoin_huobi, up)

    with open('trade_pairs_btcturk_huobi_dict.json', 'w') as tp:
        json.dump(trade_pairs_btcturk_huobi, tp)






#Get the the calculated profit orderbook
def find_arb( pair,ask_exchange,bid_exchange):


    #Combine the bid and ask exchanges
    combo = ask_exchange + '/' + bid_exchange

    orderbook_ref = ask_exchange.replace('pairs', 'orderbook')

    trade_pairs=func_arb.get_trade_pairs(combo)
    #print('Trade pairs', trade_pairs)


    #Get the selected pairs from each exchange
    selected_trade_pairs = func_arb.select_pairs(trade_pairs, pair, ask_exchange, bid_exchange)
    #print('Selected trade pairs ', selected_trade_pairs)
    if len(selected_trade_pairs[ask_exchange]) ==0:
        return 'No common trade pairs found '



    # Get a dictionary of ask and bid prices for the selected pairs
    price_dict = func_arb.sort_price( selected_trade_pairs, ask_exchange, bid_exchange)
    #print('Price dict',price_dict)


    # Get the surface profits
    surface_rate_list = func_arb.calc_surf_rate(price_dict, selected_trade_pairs, ask_exchange, bid_exchange,pair)
    #print('Surface rate list ',surface_rate_list)
    if len(surface_rate_list)==0:
        return 'No arbitrage found'


    # Get the orderbook for each pair according to the required depth
    arb_orderbook = func_arb.get_orderbook(surface_rate_list, ask_exchange, bid_exchange)
    #print('Arb orderbook ', arb_orderbook)



    # Calculate the orderbook depth
    rates= func_arb.calc_depth(arb_orderbook, ask_exchange,bid_exchange,pair)
    return rates





#'''MAIN'''

#if __name__=='__main__':
    #init_trade_pairs()

    #find_arb( pair= ['AVAX/USD'], ask_exchange='btcturk_pairs', bid_exchange='ftx_pairs')

