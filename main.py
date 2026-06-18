import json
import logging
import requests
import func_arb
import time
import random
from itertools import combinations
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)




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

    # Fetch all exchange market data in parallel
    exchange_fetchers = {
        "coinbase": (coinbase_url, func_arb.get_coinbase),
        "kraken":   (kraken_url,   func_arb.get_kraken),
        "okx":      (okx_url,      func_arb.get_okx),
        "huobi":    (huobi_url,    func_arb.get_huobi),
        "okcoin":   (okcoin_url,   func_arb.get_okcoin),
        "kucoin":   (kucoin_url,   func_arb.get_kucoin),
        "bittrex":  (bittrex_url,  func_arb.get_bittrex),
        "bitget":   (bitget_url,   func_arb.get_bitget),
        "binance":  (binance_url,  func_arb.get_binance),
    }

    tickers = {}
    with ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(func_arb.get_ticker, url): (name, parser)
            for name, (url, parser) in exchange_fetchers.items()
        }
        for future in as_completed(futures):
            name, parser = futures[future]
            try:
                tickers[name] = parser(future.result())
            except Exception as e:
                logger.error("Failed to fetch tickers for %s: %s", name, e)

    # NOTE: huobi must be last in ticker_list for find_common_pairs to work correctly
    ordered_names = ["kraken", "coinbase", "okcoin", "okx", "kucoin", "bittrex", "binance", "bitget", "huobi"]
    ticker_list = [tickers[name] for name in ordered_names if name in tickers]

    for exchange in combinations(ticker_list, 2):
        # Get the exchange key (the key that is not "sign")
        exc_1 = next(k for k in exchange[0] if k != "sign").replace("_pairs", "")
        exc_2 = next(k for k in exchange[1] if k != "sign").replace("_pairs", "")

        common_pairs = func_arb.find_common_pairs(pair_1=exchange[0], pair_2=exchange[1])

        with open(f'trade_pairs_{exc_1}_{exc_2}.json', 'w') as f:
            json.dump(common_pairs, f)

    print("Files saved!")






# Ask exchange: the exchange we BUY from
# Bid exchange: the exchange we SELL at

#Get the the calculated profit orderbook
def find_arb(pair, ask_exchange, bid_exchange):

    if ask_exchange not in exchange_dict or bid_exchange not in exchange_dict:
        logger.error("Unknown exchange: ask=%s bid=%s", ask_exchange, bid_exchange)
        return []

    combo = ask_exchange + "/" + bid_exchange

    if "kucoin" in combo and "huobi" in combo and pair[0] in red_list:
        return []

    trade_pairs = func_arb.get_trade_pairs(ask_exchange, bid_exchange)
    if trade_pairs == "":
        return []

    ask_sign = exchange_dict[ask_exchange]
    bid_sign = exchange_dict[bid_exchange]
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
    except (IndexError, TypeError, KeyError) as e:
        logger.error("find_arb error (%s/%s): %s", ask_exchange, bid_exchange, e)
        return []
    except requests.exceptions.RequestException as e:
        logger.error("find_arb network error (%s/%s): %s", ask_exchange, bid_exchange, e)
        return []




    return rates












def launcher(input_pair):

    exchanges = ["bitget", "binance", "bittrex", "kraken", "kucoin", "okx", "coinbase", "okcoin", "huobi"]
    ask_exchanges = exchanges[:]
    bid_exchanges = exchanges[:]

    random.shuffle(ask_exchanges)
    random.shuffle(bid_exchanges)

    for ask in ask_exchanges:
        for bid in bid_exchanges:
            if ask != bid:
                print("Exchanges: ", ask + "/" + bid)
                print("Pair*** ", input_pair)

                rates = find_arb(pair=[input_pair], ask_exchange=ask, bid_exchange=bid)

                if rates not in ('No common pairs', 'No arbitrage found', []):
                    print(rates)











CONCAT_SIGN_EXCHANGES = {"huobi", "bitget", "binance"}


def get_all_pairs():

    seen = set()
    all_pairs = []
    exchanges = ["kraken", "kucoin", "okx", "coinbase", "okcoin", "huobi", "bitget", "binance", "bittrex"]

    for ask in exchanges:
        for bid in exchanges:
            if ask == bid:
                continue

            common_pairs = func_arb.get_trade_pairs(ask, bid)
            if not common_pairs:
                continue

            # For concat-sign exchanges the normalised pairs are in the other exchange's key
            source_key = (bid if ask in CONCAT_SIGN_EXCHANGES else ask) + "_pairs"

            for pair in common_pairs[source_key]:
                if "/" in pair:
                    normalised = pair
                elif "-" in pair:
                    normalised = pair.replace("-", "/")
                else:
                    continue

                if normalised not in seen:
                    seen.add(normalised)
                    all_pairs.append(normalised)

    return all_pairs




def run():
    all_pairs = get_all_pairs()
    random.shuffle(all_pairs)

    for pair in all_pairs:
        time.sleep(0.3)
        launcher(input_pair=pair)


if __name__ == "__main__":
    run()





