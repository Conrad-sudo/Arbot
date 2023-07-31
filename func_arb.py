import json
import requests







fee_dict = {
        "kraken_pairs": 0.0026,
        "huobi_pairs": 0.002,
        "coinbase_pairs": 0.006,
        "okcoin_pairs": 0.002,
        "okx_pairs": 0.001,
        "kucoin_pairs": 0.001,
        "bittrex_pairs": 0.0035,
        "bitget_pairs":0.002,
        "binance_pairs":0.001
    }


# Retrieve the json object from the API
def get_ticker(url):
    url_req = requests.get(url)

    # Covert to a json object
    url_json = json.loads(url_req.text)
    return url_json




# loop through kraken object and find tradable pairs
def get_kraken(kraken_market):

    coin_list=[]
    search = kraken_market['result']

    for pair in search:
        if '/USD' in search[pair]['wsname']:
            coin_list.append(search[pair]['wsname'])
    coin_dict={"sign":"/",'kraken_pairs':coin_list}
    return coin_dict


#Loop through coinbase object to find tradable pairs
def get_coinbase(coinbase_market):
    coin_list = []

    list_items= coinbase_market['data']

    for item in list_items:
        trade_pair=item['base']+'-'+item['currency']

        coin_list.append(trade_pair)

    coin_dict={"sign":"-",'coinbase_pairs':coin_list}
    return coin_dict


#Loop through okx object to find tradable pairs
def get_okx(okx_market):

    coin_list=[]
    list_items=okx_market['data']

    for item in list_items:

        #Take out the -SWAP part
        restruct_pair= item['instId'].replace('-SWAP','')
        coin_list.append(restruct_pair)
    coin_dict={"sign":"-", 'okx_pairs': coin_list}
    return  coin_dict


#Loop through huobi object to find tradable pairs
def get_huobi(huobi_market):
    coin_list=[]
    list_items=huobi_market['data']

    for t_pair in list_items:
        if 'usd' in t_pair['symbol']:
            coin_list.append(t_pair['symbol'])
    coin_dict={"sign":"*",'huobi_pairs':coin_list}

    return coin_dict


#Loop through okcoin object to find tradable pairs
def get_okcoin(okcoin_market):

    coin_list=[]

    list_items=okcoin_market['data'][0]['instruments']

    for t_pair in list_items:
         coin_list.append(t_pair["instId"])

    coin_dict={"sign":"-",'okcoin_pairs': coin_list}
    return coin_dict



#Loop through kucoin object to find tradable pairs
def get_kucoin(kucoin_market):

    coin_list = []

    list_items = kucoin_market['data']['ticker']

    for t_pair in list_items:
        coin_list.append(t_pair["symbol"])

    coin_dict = {"sign":"-",'kucoin_pairs': coin_list}
    return coin_dict




def get_bittrex(bittrex_market):

    coins_list = []

    for ticker in bittrex_market:
        coins_list.append(ticker["symbol"])

    coin_dict={"sign":"-","bittrex_pairs":coins_list}

    return coin_dict



def get_bitget(bitget_market):

    coin_list = []

    for ticker in bitget_market["data"]:
        coin_list.append(ticker["symbol"])

    coin_dict = {"sign":"*","bitget_pairs": coin_list}

    return coin_dict




def get_binance(binance_market):


    coin_list = []

    for ticker in binance_market["symbols"]:
        coin_list.append(ticker["symbol"])

    coin_dict = {"sign": "*", "binance_pairs": coin_list}

    return coin_dict





#Find common pairs between different exchnages
def find_common_pairs(pair_1,pair_2) :

    #Get the pair names
    for pair in pair_1:
        comp_1=pair

    for pair in pair_2:
        comp_2= pair



    sign_1 = pair_1["sign"]
    sign_2 = pair_2["sign"]
    sign_combo = sign_1 + sign_2


    a_pairs = []
    b_pairs = []
    list_1 = ["/", "-", "*"]
    list_2 = ["/", "-", "*"]


    for sign_a in list_1:
        for sign_b in list_2:
            ref_combo = sign_a + sign_b

            if sign_combo == ref_combo and ref_combo == "**":

                for i_pair in pair_1[comp_1]:
                    for j_pair in pair_2[comp_2]:
                        pair_upper = j_pair.upper()
                        # print(pair_upper)
                        if i_pair == pair_upper:
                            a_pairs.append(i_pair)
                            b_pairs.append(j_pair)


            if sign_combo == ref_combo and ref_combo == "/*":

                indexer = []
                # Reconstruct huobi pairs

                for pair in pair_2[comp_2]:
                    pair_upper = pair.upper()
                    if 'HUSDT' in pair_upper:
                        new_pair = pair_upper.replace('USDT', '/USDT')
                        indexer.append((new_pair, pair))
                    elif 'HHUSD' in pair_upper:
                        new_pair = pair_upper.replace('HUSD', '/USD')
                        indexer.append((new_pair, pair))
                    elif 'USDT' in pair_upper:
                        new_pair = pair_upper.replace('USDT', '/USDT')
                        indexer.append((new_pair, pair))

                    elif 'USDC' in pair_upper:
                        new_pair = pair_upper.replace('USDC', '/USDC')
                        indexer.append((new_pair, pair))

                    elif 'EUR' in pair_upper:
                        new_pair = pair_upper.replace('EUR', '/EUR')
                        indexer.append((new_pair, pair))

                # Loop through coinbase pairs

                for i_pair in pair_1[comp_1]:
                    for j_pair in indexer:
                        if i_pair == j_pair[0]:
                            a_pairs.append(i_pair)
                            b_pairs.append(j_pair[1])

            if sign_combo == ref_combo and ref_combo == "--":

                for i_pair in pair_1[comp_1]:
                    for j_pair in pair_2[comp_2]:
                        if i_pair == j_pair:
                            a_pairs.append(i_pair)
                            b_pairs.append(j_pair)


            if sign_combo == ref_combo and ref_combo == "/-":

                for i_pair in pair_2[comp_2]:
                    restruct = i_pair.replace('-', '/')
                    for j_pair in pair_1[comp_1]:
                        if restruct == j_pair:
                            a_pairs.append(j_pair)
                            b_pairs.append(i_pair)

            if sign_combo == ref_combo and ref_combo == "-*":

                indexer = []

                for pair in pair_2[comp_2]:
                    pair_upper = pair.upper()
                    if 'HUSDT' in pair_upper:
                        new_pair = pair_upper.replace('USDT', '-USDT')
                        indexer.append((new_pair, pair))
                    elif 'HHUSD' in pair_upper:
                        new_pair = pair_upper.replace('HUSD', '-USD')
                        indexer.append((new_pair, pair))
                    elif 'USDT' in pair_upper:
                        new_pair = pair_upper.replace('USDT', '-USDT')
                        indexer.append((new_pair, pair))
                    elif 'USDC' in pair_upper:
                        new_pair = pair_upper.replace('USDC', '-USDC')
                        indexer.append((new_pair, pair))
                    elif 'EUR' in pair_upper:
                        new_pair = pair_upper.replace('EUR', '/EUR')
                        indexer.append((new_pair, pair))

                    # Loop through coinbase pairs

                for i_pair in pair_1[comp_1]:
                    for j_pair in indexer:
                        if i_pair == j_pair[0]:
                            a_pairs.append(i_pair)
                            b_pairs.append(j_pair[1])


    trade_pairs = {comp_1: a_pairs, comp_2: b_pairs}

    return trade_pairs






#retreive a trade pair from the json trade pairs
def get_trade_pairs(ask_exchange,bid_exchange):

    # Get the tradable pair dictionary according to the ask and bid exchanges. Just add the name of the exchange to the two lists

    list_1 = ["bittrex", "coinbase", "kucoin", "okx", "okcoin", "huobi", "kraken","bitget","binance"]
    list_2 = ["bittrex", "coinbase", "kucoin", "okx", "okcoin", "huobi", "kraken","bitget","binance"]

    combo = ask_exchange + "/" + bid_exchange

    trade_pairs = ""

    for exc_1 in list_1:
        for exc_2 in list_2:
            if exc_1 != exc_2:
                ref_combo = exc_1 + "/" + exc_2
                if combo == ref_combo:

                    try:
                        f = open(f'trade_pairs_{exc_1}_{exc_2}.json')

                    except:
                        f = open(f'trade_pairs_{exc_2}_{exc_1}.json')

                    trade_pairs = json.load(f)
                    f.close()

    return trade_pairs




# Create a new list for selected coins pairs
def select_pairs(trade_pairs, pair,ask_exchange,bid_exchange,ask_sign,bid_sign):


    sign_combo = ask_sign + bid_sign
    ask_exc_pairs = trade_pairs[ask_exchange]
    bid_exc_pairs = trade_pairs[bid_exchange]
    selected_ask_exc_pairs = []
    selected_bid_exc_pairs = []

    list_1=["/","-","*"]
    list_2=["/","-","*"]

    for p in pair:

        ref = p.split("/")

        for sign_1 in list_1:
            for sign_2 in list_2:

                ref_sign = sign_1 + sign_2

                for i in range(0, len(ask_exc_pairs)):

                    if sign_combo == ref_sign and ref_sign == "/-":
                        exc_ref = bid_exc_pairs[i].split("-")

                    elif sign_combo == ref_sign and ref_sign == "-/":
                        exc_ref = ask_exc_pairs[i].split("-")

                    elif sign_combo == ref_sign and ref_sign == "*/":
                        exc_ref = bid_exc_pairs[i].split("/")

                    elif sign_combo == ref_sign and ref_sign == "/*":
                        exc_ref = ask_exc_pairs[i].split("/")

                    elif sign_combo == ref_sign and ref_sign == "-*":
                        exc_ref = ask_exc_pairs[i].split("-")

                    elif sign_combo == ref_sign and ref_sign == "*-":
                        exc_ref = bid_exc_pairs[i].split("-")

                    elif sign_combo == ref_sign and ref_sign == "--":
                        exc_ref = ask_exc_pairs[i].split("-")

                    elif sign_combo == ref_sign and ref_sign == "**":
                        exc_ref = ask_exc_pairs[i].upper()
                        other_exc_ref = bid_exc_pairs[i].upper()

                    else:
                        break

                    if type(exc_ref) == list:
                        if ref[0] == exc_ref[0] and ref[1] == exc_ref[1]:
                            selected_ask_exc_pairs.append(trade_pairs[ask_exchange][i])
                            selected_bid_exc_pairs.append(trade_pairs[bid_exchange][i])

                    elif type(exc_ref) == str:
                        new_ref=ref[0]+ref[1]
                        if exc_ref == other_exc_ref and exc_ref==new_ref:
                            selected_ask_exc_pairs.append(trade_pairs[ask_exchange][i])
                            selected_bid_exc_pairs.append(trade_pairs[bid_exchange][i])




    selected_trade_pairs = {bid_exchange: selected_bid_exc_pairs, ask_exchange: selected_ask_exc_pairs}

    return selected_trade_pairs





# Form a dictionary of bid an ask prices for the selected pairs on both exchanges
def sort_price( selected_trade_pairs,bid_exchange,ask_exchange):

    coinbase_price_list= []
    kraken_price_list =[]
    okx_prices_list=[]
    okcoin_prices_list=[]
    huobi_prices_list=[]
    kucoin_prices_list=[]
    bittrex_prices_list=[]
    bitget_prices_list=[]
    binance_prices_list=[]
    price_dict = {}






    try:
        #Get the bid and ask price for every pair from coinbase
        if bid_exchange=='coinbase_pairs' or ask_exchange=='coinbase_pairs':


            for t_pair in selected_trade_pairs['coinbase_pairs']:

                data = get_ticker(f"https://api.exchange.coinbase.com/products/{t_pair}/ticker")
                ask = data["ask"]
                bid = data["bid"]
                prices = {'bid': bid, 'ask': ask}
                coinbase_price_list.append(prices)

            price_dict.update({'coinbase_pairs':coinbase_price_list})


        if bid_exchange=='kraken_pairs' or ask_exchange=='kraken_pairs':

            for t_pair in selected_trade_pairs['kraken_pairs']:
                data = get_ticker(f"https://api.kraken.com/0/public/Ticker?pair={t_pair}")["result"][t_pair]
                ask = data["a"][0]
                bid = data["b"][0]
                prices={ 'bid':bid, 'ask':ask}
                kraken_price_list.append(prices)
            price_dict.update({'kraken_pairs':kraken_price_list})


        if bid_exchange=='okx_pairs' or ask_exchange=='okx_pairs':

            for t_pair in selected_trade_pairs['okx_pairs']:

                ticker_prices= get_ticker(f'https://www.okx.com/api/v5/market/ticker?instId={t_pair}-SWAP')
                ask=float(ticker_prices['data'][0]["askPx"])
                bid=float(ticker_prices['data'][0]["bidPx"])
                prices={'bid':bid,'ask':ask}
                okx_prices_list.append(prices)
            price_dict.update({'okx_pairs':okx_prices_list})

        if bid_exchange == 'okcoin_pairs' or ask_exchange == 'okcoin_pairs':

            for t_pair in selected_trade_pairs['okcoin_pairs']:
                ticker_prices = get_ticker(f'https://www.okcoin.com/api/v5/market/ticker?instId={t_pair}')
                ask = float(ticker_prices["data"][0]["askPx"])
                bid = float(ticker_prices["data"][0]["bidPx"])
                prices = {'bid': bid, 'ask': ask}
                okcoin_prices_list.append(prices)
            price_dict.update({'okcoin_pairs': okcoin_prices_list})


        if bid_exchange == 'binance_pairs' or ask_exchange == 'binance_pairs':

            for t_pair in selected_trade_pairs['binance_pairs']:
                ticker_prices = get_ticker(f"https://api.binance.com/api/v3/ticker/bookTicker?symbol={t_pair}")
                ask = float(ticker_prices["askPrice"])
                bid = float(ticker_prices["bidPrice"])
                prices = {'bid': bid, 'ask': ask}
                binance_prices_list.append(prices)
            price_dict.update({'binance_pairs': binance_prices_list})


        if bid_exchange=='huobi_pairs' or ask_exchange =='huobi_pairs':

            for t_pair in selected_trade_pairs['huobi_pairs']:
                ticker_prices= get_ticker(f'https://api.huobi.pro/market/detail/merged?symbol={t_pair}')
                ask= float(ticker_prices['tick']['ask'][0])
                bid= float(ticker_prices['tick']['bid'][0])
                prices = {'bid': bid, 'ask': ask}
                huobi_prices_list.append(prices)
            price_dict.update({'huobi_pairs': huobi_prices_list})



        if bid_exchange=="bittrex_pairs" or ask_exchange=="bittrex_pairs":
            for t_pair in selected_trade_pairs['bittrex_pairs']:
                ticker_prices = get_ticker(f"https://api.bittrex.com/v3/markets/{t_pair}/ticker")
                ask = float(ticker_prices["askRate"])
                bid = float(ticker_prices["bidRate"])
                prices = {'bid': bid, 'ask': ask}
                bittrex_prices_list.append(prices)
            price_dict.update({'bittrex_pairs': bittrex_prices_list})

        if bid_exchange=="bitget_pairs" or ask_exchange=="bitget_pairs":

            for t_pair in selected_trade_pairs['bitget_pairs']:

                ticker_prices = get_ticker(f"https://api.bitget.com/api/spot/v1/market/ticker?symbol={t_pair}_SPBL")

                ask = float(ticker_prices["data"]["sellOne"])
                bid = float(ticker_prices["data"]["buyOne"])
                prices = {'bid': bid, 'ask': ask}
                bitget_prices_list.append(prices)
            price_dict.update({'bitget_pairs': bitget_prices_list})




        if bid_exchange=="kucoin_pairs" or ask_exchange=="kucoin_pairs":

            ticker_prices=get_ticker("https://api.kucoin.com/api/v1/market/allTickers")["data"]["ticker"]
            for t_pair in selected_trade_pairs['kucoin_pairs']:
                for ticker in ticker_prices:
                    if t_pair==ticker["symbol"]:
                        ask=float(ticker["sell"])
                        bid=float(ticker["buy"])
                        prices={"bid":bid,"ask":ask}
                        kucoin_prices_list.append(prices)

                        break

            price_dict.update({"kucoin_pairs":kucoin_prices_list})

        return price_dict

    except KeyError:
        return []
    except IndexError:
        return []








# Calculate the surface rate
def calc_surf_rate(price_dict, selected_trade_pairs, ask_exchange,bid_exchange):


    counter = 0
    surf_rate_list = []
    ask_price_list=price_dict[ask_exchange]
    bid_price_list = price_dict[bid_exchange]


    while counter < len(ask_price_list):

        #ask_price_list_bid = float(ask_price_list[counter]['bid'])
        ask_price_list_ask = float(ask_price_list[counter]['ask'])
        bid_price_list_bid = float(bid_price_list[counter]['bid'])
        #bid_price_list_ask = float(bid_price_list[counter]['ask'])


        #When none of the exchanges are Turkish
        if  ask_price_list_ask< bid_price_list_bid :
            bid_exchange_pairs = selected_trade_pairs[bid_exchange][counter]
            ask_exchange_pairs = selected_trade_pairs[ask_exchange][counter]
            stats = {ask_exchange: ask_exchange_pairs, bid_exchange: bid_exchange_pairs}
            surf_rate_list.append(stats)

        counter += 1

    return surf_rate_list





# Retrieve the orderbook for each pair in the list
def get_orderbook(surface_rate_list, ask_exchange, bid_exchange, depth):

    arb_orderbook={}
    coinbase_orderbook=[]
    kraken_orderbook=[]
    okx_orderbook=[]
    okcoin_orderbook=[]
    huobi_orderbook=[]
    kucoin_orderbook=[]
    bittrex_orderbook=[]
    bitget_orderbook=[]
    binance_orderbook=[]



    # Get the orderbook for each pair in each exchange

    try:



        if ask_exchange == 'coinbase_pairs' or bid_exchange == 'coinbase_pairs':

            for pair in surface_rate_list:
                coinbase_pair = pair['coinbase_pairs']
                coinbase_url = f'https://api.exchange.coinbase.com/products/{coinbase_pair}/book?level=2'
                raw_book = get_ticker(coinbase_url)
                # Recontruct the book for first 100 entries
                bids = raw_book['bids'][0:depth]
                asks = raw_book['asks'][0:depth]
                book = {'bids': bids, 'asks': asks}
                coinbase_orderbook.append([coinbase_pair, book])
            arb_orderbook.update({'coinbase_orderbook': coinbase_orderbook})


        if ask_exchange == 'bittrex_pairs' or bid_exchange == 'bittrex_pairs':

            for pair in surface_rate_list:

                bids = []
                asks = []
                bittrex_pair = pair['bittrex_pairs']
                raw_book = get_ticker(f"https://api.bittrex.com/v3/markets/{bittrex_pair}/orderbook?depth=500")
                # Recontruct the book for first 100 entries
                ref_bids = raw_book['bid'][0:depth]
                ref_asks = raw_book['ask'][0:depth]

                for entry in ref_bids:
                    bids.append([entry["rate"], entry["quantity"]])

                for entry in ref_asks:
                    asks.append([entry["rate"], entry["quantity"]])

                book = {'bids': bids, 'asks': asks}
                bittrex_orderbook.append([bittrex_pair, book])


            arb_orderbook.update({'bittrex_orderbook': bittrex_orderbook})


        if ask_exchange == 'kraken_pairs' or bid_exchange == 'kraken_pairs':

            for pair in surface_rate_list:
                kraken_pair = pair['kraken_pairs']
                data=get_ticker(f"https://api.kraken.com/0/public/Depth?pair={kraken_pair}")["result"][kraken_pair]
                asks=data["asks"][0:depth]
                bids=data["bids"][0:depth]
                book = {'bids': bids, 'asks': asks}
                kraken_orderbook.append([kraken_pair, book])
            arb_orderbook.update({'kraken_orderbook': kraken_orderbook})

        if ask_exchange == 'binance_pairs' or bid_exchange == 'binance_pairs':

            for pair in surface_rate_list:
                binance_pair = pair['binance_pairs']
                data=get_ticker(f"https://api.binance.com/api/v3/depth?symbol={binance_pair}")
                asks = data["asks"][0:depth]
                bids = data["bids"][0:depth]
                book = {'bids': bids, 'asks': asks}
                binance_orderbook.append([binance_pair, book])
            arb_orderbook.update({'binance_orderbook': binance_orderbook})



        if ask_exchange == 'okx_pairs' or bid_exchange == 'okx_pairs':

            for t_pair in surface_rate_list:
                okx_pair = t_pair['okx_pairs']
                data = get_ticker(f'https://www.okx.com/api/v5/market/books?instId={okx_pair}&sz={depth}')['data'][0]
                asks=data["asks"]
                bids=data["bids"]
                book = {'bids': bids, 'asks': asks}
                okx_orderbook.append([okx_pair, book])
            arb_orderbook.update({'okx_orderbook': okx_orderbook})


        if ask_exchange == 'okcoin_pairs' or bid_exchange == 'okcoin_pairs':

            for t_pair in surface_rate_list:
                okcoin_pair = t_pair['okcoin_pairs']
                data=get_ticker(f'https://www.okcoin.com/api/v5/market/books?instId={okcoin_pair}&sz={depth}')
                asks = data["data"][0]["asks"]
                bids = data["data"][0]["bids"]
                book = {'bids': bids, 'asks': asks}
                okcoin_orderbook.append([okcoin_pair, book])
            arb_orderbook.update({'okcoin_orderbook': okcoin_orderbook})

        if ask_exchange=='huobi_pairs' or bid_exchange=='huobi_pairs':

            for t_pair in surface_rate_list:
                huobi_pair = t_pair['huobi_pairs']
                raw_orderbook = get_ticker(f'https://api.huobi.pro/market/depth?symbol={huobi_pair}&type=step0')
                bids = raw_orderbook['tick']['bids'][0:depth]
                asks = raw_orderbook['tick']['asks'][0:depth]
                book={'bids':bids, 'asks':asks}
                huobi_orderbook.append([huobi_pair,book])
            arb_orderbook.update({'huobi_orderbook':huobi_orderbook})

        if ask_exchange=="kucoin_pairs" or bid_exchange=="kucoin_pairs":

            for t_pair in surface_rate_list:
                kucoin_pair= t_pair["kucoin_pairs"]
                raw_orderbook=get_ticker(f"https://api.kucoin.com/api/v1/market/orderbook/level2_100?symbol={kucoin_pair}")
                bids=raw_orderbook["data"]["bids"][0:depth]
                asks=raw_orderbook["data"]["asks"][0:depth]
                book={'bids':bids, 'asks':asks}
                kucoin_orderbook.append([kucoin_pair,book])

            arb_orderbook.update({'kucoin_orderbook':kucoin_orderbook})


        if ask_exchange=="bitget_pairs" or bid_exchange=="bitget_pairs":

            for t_pair in surface_rate_list:
                bitget_pair= t_pair["bitget_pairs"]
                raw_orderbook=get_ticker(f"https://api.bitget.com/api/spot/v1/market/depth?symbol={bitget_pair}_SPBL&type=step0&limit=100")
                bids=raw_orderbook["data"]["bids"][0:depth]
                asks=raw_orderbook["data"]["asks"][0:depth]
                book={'bids':bids, 'asks':asks}
                bitget_orderbook.append([bitget_pair,book])

            arb_orderbook.update({'bitget_orderbook':bitget_orderbook})





        return arb_orderbook


    except IndexError:
        return []






# Calculate the profit based on orderbook depth
def calc_depth(arb_orderbook,ask_exchange,bid_exchange):



    combo = ask_exchange + '/' + bid_exchange
    counter = 0
    depth_rate_list = []
    global message
    global table
    orderbook_ref = ask_exchange.replace('pairs', 'orderbook')

    #Doesnt matter how you add the exchnages here
    list_1 = ["bittrex_pairs", "coinbase_pairs", "kucoin_pairs", "okx_pairs", "okcoin_pairs", "huobi_pairs","kraken_pairs","bitget_pairs","binance_pairs"]
    list_2 = ["bittrex_pairs", "coinbase_pairs", "kucoin_pairs", "okx_pairs", "okcoin_pairs", "huobi_pairs","kraken_pairs","bitget_pairs","binance_pairs"]





    ask_orderbook=""
    bid_orderbook=""


    #Get the orderbooks by looping thouhgh lists
    for ask_exc in list_1:
        for bid_exc in list_2:

            if ask_exc !=bid_exc:
                ref= ask_exc+"/"+bid_exc

                if ref==combo:
                    ask_exc_ob= ask_exc.replace("pairs","orderbook")
                    bid_exc_ob= bid_exc.replace("pairs","orderbook")
                    ask_orderbook=arb_orderbook[ask_exc_ob]
                    bid_orderbook=arb_orderbook[bid_exc_ob]




    # Loop through the orderbook
    while counter < len(arb_orderbook[orderbook_ref]):


        # Get pair name
        pair_name =  arb_orderbook[orderbook_ref][counter][0]
        # Set the orderbook
        orderbook = []


        # Get the ask prices /// returns an array of arrays
        ask_prices = ask_orderbook[counter][1]['asks']
        # Get the bid prices /// returns an array of arrays
        bid_prices = bid_orderbook[counter][1]['bids']




        price_counter = 0



        #Calculatre the profit levels
        while price_counter < len(bid_prices):

            #Both foreign exchanges
            ask = float(ask_prices[price_counter][0])
            bid = float(bid_prices[price_counter][0])

            #Calculate the profit levels
            for ask_exc in list_1:
                for bid_exc in list_2:

                    if ask_exchange == ask_exc and bid_exchange == bid_exc:
                        profit = (bid * (1 - fee_dict[bid_exchange])) - (ask * (1 + fee_dict[ask_exchange]))
                        profit_perc = (profit / ask) * 100
                        break


            orderbook_position=price_counter+1

            #get the appropriate volume

            if float(bid_prices[price_counter][1]) > float(ask_prices[price_counter][1]):
                vol = float(ask_prices[price_counter][1])
            else:
                vol = float(bid_prices[price_counter][1])

            # Check for minimum profit

            if orderbook_position <= 5 :
                #Add the
                orderbook.append((ask, bid, vol, profit_perc,orderbook_position))


            price_counter += 1

        #print("orderbook ",orderbook)

        if len(orderbook)==0:
            return []

        #else:
           # print("orderbook ",orderbook)

        #Get the total volume
        total_vol = 0
        total_ask_price=0
        total_bid_price=0
        total_weight=0

        for i in orderbook:
            total_vol += i[2]
            total_weight+=i[2]*i[3]
            total_ask_price+=i[0]*i[2]
            total_bid_price+=i[1]*i[2]

        weighted_profit=total_weight/total_vol


        weighted_profit = "{:.2f}".format(weighted_profit)
        total_ask_price="{:.2f}".format(total_ask_price)
        total_bid_price="{:.2f}".format(total_bid_price)

        ask_1 = orderbook[0][0]

        bid_1 = orderbook[0][1]




        ask_ref= ask_exchange.replace('_pairs','')
        bid_ref=bid_exchange.replace('_pairs','')


        message= f"pair: {pair_name}\n" \
                 f"buy exc: {ask_ref}\n" \
                 f"sell exc: {bid_ref}\n" \
                 f"buy: {ask_1 }\n" \
                 f"sell: {bid_1}\n" \
                 f"buy USD: {total_ask_price}\n" \
                 f"sell USD: {total_bid_price}\n" \
                 f"vol: {total_vol}\n" \
                 f"wei prof%: {weighted_profit}\n"





        depth_rate_list.append(message)

        counter += 1

    return message







