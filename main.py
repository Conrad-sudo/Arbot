import json
import func_arb
import time
import random
from itertools import combinations




coinbase_url = 'https://api.coinbase.com/v2/prices/usd/spot'
kraken_url='https://api.kraken.com/0/public/AssetPairs?'
okx_url='https://www.okx.com/api/v5/market/tickers?instType=SWAP'
huobi_url='https://api.huobi.pro/market/tickers'
okcoin_url='https://www.okcoin.com/api/v3/otc/rfq/instruments'
kucoin_url="https://api.kucoin.com/api/v1/market/allTickers"
bittrex_url="https://api.bittrex.com/v3/markets"
bitget_url="https://api.bitget.com/api/spot/v1/market/tickers"
binance_url="https://api.binance.com/api/v3/exchangeInfo"


exchange_dict={
    "kraken":"/",
    "coinbase":"-",
    "kucoin":"-",
    "okcoin":"-",
    "huobi":"*",
    "bittrex":"-",
    "bitget":"*",
    "okx":"-",
    "binance":"*"
}

red_list=["XNO/USDT","MC/USDT","SOUL/USDT","STC/USDT","HTR/USDT","ACA/USDT","LOVE/USDT","KAI/USDT","SRM/USDT","DYP/USDT"]

#Initialise the tradable pairs between exchanges
def init_trade_pairs():


    # retrieve json objects from APIs
    coinbase_market = func_arb.get_ticker(coinbase_url)
    kraken_market=func_arb.get_ticker(kraken_url)
    okx_market=func_arb.get_ticker(okx_url)
    huobi_market=func_arb.get_ticker(huobi_url)
    okcoin_market=func_arb.get_ticker(okcoin_url)
    kucoin_market=func_arb.get_ticker(kucoin_url)
    bittrex_market=func_arb.get_ticker(bittrex_url)
    bitget_market=func_arb.get_ticker(bitget_url)
    binance_market=func_arb.get_ticker(binance_url)


    #Get the tickers for each pair in the exchanges .Functions are unique because exchanges have different APIs
    okcoin_tickers = func_arb.get_okcoin(okcoin_market)
    kraken_tickers=func_arb.get_kraken(kraken_market)
    coinbase_tickers=func_arb.get_coinbase(coinbase_market)
    okx_tickers=func_arb.get_okx(okx_market)
    huobi_tickers=func_arb.get_huobi(huobi_market)
    kucoin_tickers=func_arb.get_kucoin(kucoin_market)
    bittrex_tickers=func_arb.get_bittrex(bittrex_market)
    bitget_tickers=func_arb.get_bitget(bitget_market)
    binance_tickers=func_arb.get_binance(binance_market)




    #list the tickers NOTE huobi should always be in last position !
    ticker_list=[kraken_tickers,coinbase_tickers,okcoin_tickers,okx_tickers,kucoin_tickers,bittrex_tickers,binance_tickers,bitget_tickers,huobi_tickers]

    combo_list = list()

    #combine the tickers in unique pairs of 2
    combo_list += list(combinations(ticker_list, 2))

    for exchange in combo_list:
        #print(exchange[0], " ", exchange[1])

        # Get the pair names
        for pair in exchange[0]:
            exc_1 = pair.replace("_pairs","")

        for pair in exchange[1]:
            exc_2 = pair.replace("_pairs","")


        common_pairs=func_arb.find_common_pairs(pair_1=exchange[0],pair_2=exchange[1])

        with open(f'trade_pairs_{exc_1}_{exc_2}.json', 'w') as f:
            json.dump(common_pairs, f)
        f.close()


    print("Files saved!")






"Ask exchange: the exchange we BUY from"
"Bid exchange : the exchange we SELL at"

#Get the the calculated profit orderbook
def find_arb( pair,ask_exchange,bid_exchange):


    combo=ask_exchange+"/"+bid_exchange

    if "kucoin" in combo and "huobi" in combo and pair[0] in red_list:
        return []

    #1
    trade_pairs=func_arb.get_trade_pairs(ask_exchange , bid_exchange)
    if trade_pairs =="":
        return []

    #print('****Trade pairs**** ', trade_pairs)

    ask_sign=exchange_dict[ask_exchange]
    bid_sign=exchange_dict[bid_exchange]
    ask_exchange = ask_exchange + "_pairs"
    bid_exchange = bid_exchange + "_pairs"



    # 2 Get the selected pairs from each exchange
    selected_trade_pairs = func_arb.select_pairs(trade_pairs, pair, ask_exchange, bid_exchange,ask_sign,bid_sign)
    #print('Selected trade pairs ', selected_trade_pairs)



    if len(selected_trade_pairs[ask_exchange]) ==0:
        return 'No common pairs'


    #3 Get a dictionary of ask and bid prices for the selected pairs
    price_dict = func_arb.sort_price( selected_trade_pairs, ask_exchange, bid_exchange)


    if len(price_dict)==0:
        return []
    #print('****Price dict****\n',price_dict)

    try:
        # Get the surface profits
        surface_rate_list = func_arb.calc_surf_rate(price_dict, selected_trade_pairs, ask_exchange, bid_exchange)

        if len(surface_rate_list)==0:
            return 'No arbitrage found'



        # Get the orderbook for each pair according to the required depth
        arb_orderbook = func_arb.get_orderbook(surface_rate_list, ask_exchange, bid_exchange,depth=100)
        #print('****Arb orderbook **** \n', arb_orderbook)
        if len(arb_orderbook)==0:
            return 'No arbitrage found'


    # Calculate the orderbook depth

        rates= func_arb.calc_depth(arb_orderbook, ask_exchange,bid_exchange)
    except IndexError:
        return []
    except TypeError:
        return []
    except KeyError:
        return []




    return rates












#init_trade_pairs()

#rates=find_arb( pair= ["APE/USDT"], ask_exchange="kraken", bid_exchange='okx')

#print(rates)


def launcher(input_pair):

    ask_exchanges=["bitget","binance","bittrex","kraken","kucoin","okx","coinbase","okcoin","huobi"]
    bid_exchages=["bitget","binance","bittrex","okx","kraken","kucoin","coinbase","okcoin","huobi"]

    random.shuffle(ask_exchanges)
    random.shuffle(bid_exchages)

    for ask in ask_exchanges:
        for bid in bid_exchages:

            if ask != bid:

                combo=ask +"/"+bid
                print("Exchanges: ",combo)
                print("Pair*** ",input_pair )

                rates= find_arb( pair=[input_pair], ask_exchange=ask, bid_exchange=bid)

                if rates=='No common pairs' or rates=='No arbitrage found' or rates==[]:
                    pass

                else:
                    print(rates)











def get_all_pairs():

    all_pairs=[]
    ask_exchanges = ["kraken", "kucoin", "okx", "coinbase", "okcoin", "huobi","bitget","binance","bittrex"]
    bid_exchages = ["okx", "kraken", "kucoin", "coinbase", "okcoin", "huobi","bitget","binance","bittrex"]

    for ask in ask_exchanges:
        for bid in bid_exchages:
            if ask != bid:
                ask_pair=ask+"_pairs"
                bid_pair=bid+"_pairs"

                common_pairs=func_arb.get_trade_pairs(ask,bid)

                if ask !="huobi" and ask != "bitget" and ask !="binance":
                    for pair in common_pairs[ask_pair]:

                        if "/" in pair and pair not in all_pairs:
                            all_pairs.append(pair)

                        if "-" in pair :
                            new=pair.replace("-","/")

                            if new not in all_pairs:
                                all_pairs.append(new)
                            else:
                                pass

                else:

                    for pair in common_pairs[bid_pair]:

                        if "/" in pair and pair not in all_pairs:
                            all_pairs.append(pair)

                        if "-" in pair:
                            new = pair.replace("-", "/")

                            if new not in all_pairs:
                                all_pairs.append(new)
                            else:
                                pass


    return all_pairs




def run ():
    all_pairs=get_all_pairs()
    random.shuffle(all_pairs)
    #print(all_pairs)

    for pair in all_pairs:
        #print("Pair**\n",pair)
        #rates=find_arb( pair= [pair], ask_exchange="kraken", bid_exchange='okx')
        time.sleep(0.3)
        launcher(input_pair=pair)



run()





