import json
import krakenex
import requests
import pandas as pd
from pykrakenapi import KrakenAPI
from coinbase.wallet.client import Client

ftx_url = 'https://ftx.com/api/markets'
liverates_url='https://www.live-rates.com/rates'
btcturk_url = 'https://api.btcturk.com/api/v2/ticker'
coinbase_url = 'https://api.coinbase.com/v2/prices/usd/spot'
#okx_url='https://www.okx.com/api/v5/market/tickers?instType=SWAP'
alpha_rates_usd_url='https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=TRY&apikey=AE966LKHL236KP1K'
alpha_rates_usdt_url='https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USDT&to_currency=TRY&apikey=AE966LKHL236KP1K'
alpha_rates_usdc_url='https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USDC&to_currency=TRY&apikey=AE966LKHL236KP1K'




# Retrieve the json object from the API
def get_ticker(url):
    url_req = requests.get(url)

    # Covert to a json object
    url_json = json.loads(url_req.text)
    return url_json



# loop through btcturk object and find tradable pairs
def get_btcturk(btcturk_market):
    coin_list = []
    for pair in btcturk_market["data"]:
        pair_name = pair["pairNormalized"]
        if 'TRY' in pair_name:
            coin_list.append(pair_name)

    coin_dict={'btcturk_pairs':coin_list}
    return coin_dict



def get_ftx(ftx_market):
    coin_list = []
    for pair in ftx_market["result"]:

        name = pair['name']
        is_enabled = pair["enabled"]
        is_postOnly = pair["postOnly"]
        is_restricted = pair["restricted"]
        base = pair["baseCurrency"]
        quote = pair['quoteCurrency']

        if is_enabled == True and is_postOnly == False and is_restricted == False and base != None and quote != None and '/USD' in name:
            coin_list.append(name)

    coin_dict={'ftx_pairs': coin_list}
    return coin_dict



# loop through kraken object and find tradable pairs
def get_kraken(kraken_market):

    coin_list=[]
    search = kraken_market['result']

    for pair in search:
        if '/USD' in search[pair]['wsname']:
            coin_list.append(search[pair]['wsname'])
    coin_dict={'kraken_pairs':coin_list}
    return coin_dict



#Loop through coinbase object to find tradable pairs
def get_coinbase(coinbase_market):
    coin_list = []

    list_items= coinbase_market['data']

    for item in list_items:
        trade_pair=item['base']+'-'+item['currency']

        coin_list.append(trade_pair)

    coin_dict={'coinbase_pairs':coin_list}
    return coin_dict


#Loop through okx object to find tradable pairs
def get_okx(okx_market):

    coin_list=[]
    list_items=okx_market['data']

    for item in list_items:

        #Take out the -SWAP part
        restruct_pair= item['instId'].replace('-SWAP','')
        coin_list.append(restruct_pair)
    coin_dict={ 'okx_pairs': coin_list}
    return  coin_dict



#Loop through huobi object to find tradable pairs
def get_huobi(huobi_market):
    coin_list=[]
    list_items=huobi_market['data']

    for t_pair in list_items:
        if 'usd' in t_pair['symbol']:
            coin_list.append(t_pair['symbol'])
    coin_dict={'huobi_pairs':coin_list}

    return coin_dict



def get_okcoin(okcoin_market):

    coin_list=[]

    list_items=okcoin_market['data'][0]['instruments']

    for t_pair in list_items:
         coin_list.append(t_pair["instId"])

    coin_dict={'okcoin_pairs': coin_list}
    return coin_dict




# Loop through the liverates  object and find the try/usd pair NB You wont have to use this after you get the API keys
def get_liverate(liverates_market, forex_pair):
    liverate_ticker = {}

    for pair in liverates_market:
        if pair['currency'] == forex_pair:
            liverate_ticker.update(pair)

    return liverate_ticker



#Temporary function to replace liverates
def get_alpha_rate(alpha_rates_market):


    alpha_rates_ticker={'bid':alpha_rates_market["Realtime Currency Exchange Rate"]["8. Bid Price"],'ask':alpha_rates_market["Realtime Currency Exchange Rate"]["9. Ask Price"] }
    return alpha_rates_ticker



#Find common pairs between different exchnages
def find_common_pairs(pair_1,pair_2) :

    #Get the pair names
    for pair in pair_1:
        comp_1=pair

    for pair in pair_2:
        comp_2= pair

    #Combine them
    combo=comp_1+'/'+comp_2


    if combo== 'kraken_pairs/ftx_pairs':

        ftx_pairs= []
        kraken_pairs=[]
        for i_pair in pair_1[comp_1]:
            for j_pair in pair_2[comp_2]:
                if i_pair==j_pair:
                    kraken_pairs.append(i_pair)
                    ftx_pairs.append(j_pair)
        trade_pairs={comp_1:kraken_pairs,comp_2:ftx_pairs}
        return trade_pairs


    elif combo=='kraken_pairs/btcturk_pairs':

        btcturk_pairs = []
        kraken_pairs = []
        indexer = []

        # itirate through btcturk pairs
        for i_pair in pair_2[comp_2]:
            # make a new list thats an indexer

            new_pair_usd = i_pair.replace('_TRY', '/USD')
            new_pair_usdt = i_pair.replace('_TRY', '/USDT')
            new_pair_usdc= i_pair.replace('_TRY', '/USDC')
            normal_pair = i_pair
            indexer.append((new_pair_usd, new_pair_usdt,new_pair_usdc, normal_pair))

        # itirate through kraken pairs
        for j_pair in pair_1[comp_1]:
            for i_pair in indexer:
                if j_pair == i_pair[0]:
                    btcturk_pairs.append(i_pair[3])
                    kraken_pairs.append(j_pair)
                elif j_pair == i_pair[1]:
                    btcturk_pairs.append(i_pair[3])
                    kraken_pairs.append(j_pair)
                elif j_pair == i_pair[2]:
                    btcturk_pairs.append(i_pair[3])
                    kraken_pairs.append(j_pair)

        trade_pairs = {comp_1: kraken_pairs, comp_2: btcturk_pairs}
        return trade_pairs


    elif combo == 'kraken_pairs/coinbase_pairs':
        coinbase_pairs=[]
        kraken_pairs=[]

        for i_pair in pair_2[comp_2]:
            restruct=i_pair.replace('-','/')
            for j_pair in pair_1[comp_1]:
                if restruct == j_pair:
                    kraken_pairs.append(j_pair)
                    coinbase_pairs.append(i_pair)
        trade_pairs= {comp_1:kraken_pairs, comp_2:coinbase_pairs}
        return trade_pairs


    elif combo=='ftx_pairs/btcturk_pairs':
        btcturk_pairs = []
        ftx_pairs = []
        indexer = []

        # itirate through btcturk pairs
        for i_pair in pair_2[comp_2]:
            # make a new list thats an indexer

            new_pair_usd = i_pair.replace('_TRY', '/USD')
            new_pair_usdt = i_pair.replace('_TRY', '/USDT')
            normal_pair = i_pair
            indexer.append((new_pair_usd, new_pair_usdt, normal_pair))

        # itirate through ftx pairs
        for j_pair in pair_1[comp_1]:
            for i_pair in indexer:
                if j_pair == i_pair[0]:
                    btcturk_pairs.append(i_pair[2])
                    ftx_pairs.append(j_pair)
                elif j_pair == i_pair[1]:
                    print(j_pair)
                    btcturk_pairs.append(i_pair[2])
                    ftx_pairs.append(j_pair)

        trade_pairs = {comp_1: ftx_pairs, comp_2: btcturk_pairs}
        return trade_pairs


    elif combo== 'ftx_pairs/coinbase_pairs':
        ftx_pairs=[]
        coinbase_pairs=[]

        for i_pair in pair_2[comp_2]:
            restruct=i_pair.replace('-','/')
            for j_pair in pair_1[comp_1]:
                if restruct == j_pair:
                    ftx_pairs.append(j_pair)
                    coinbase_pairs.append(i_pair)
        trade_pairs= {comp_1:ftx_pairs, comp_2:coinbase_pairs}
        return trade_pairs


    elif combo=='btcturk_pairs/coinbase_pairs':
        btcturk_pairs=[]
        coinbase_pairs=[]

        for i_pair in pair_2[comp_2]:
            restruct = i_pair.replace('-USD', '_TRY')
            for j_pair in pair_1[comp_1]:
                if restruct == j_pair:
                    btcturk_pairs.append(j_pair)
                    coinbase_pairs.append(i_pair)
        trade_pairs = {comp_1: btcturk_pairs, comp_2: coinbase_pairs}
        return trade_pairs


    elif combo=='ftx_pairs/okx_pairs':
        ftx_pairs= []
        okx_pairs=[]

        for i_pair in pair_2[comp_2]:
            restruct = i_pair.replace('-', '/')
            for j_pair in pair_1[comp_1]:
                if restruct == j_pair:
                    ftx_pairs.append(j_pair)
                    okx_pairs.append(i_pair)
        trade_pairs = {comp_1: ftx_pairs, comp_2: okx_pairs}
        return trade_pairs


    elif combo == 'coinbase_pairs/okx_pairs':

        okx_pairs = []
        coinbase_pairs = []
        for i_pair in pair_1[comp_1]:
            for j_pair in pair_2[comp_2]:
                if i_pair == j_pair:
                    coinbase_pairs.append(i_pair)
                    okx_pairs.append(j_pair)
        trade_pairs = {comp_1: coinbase_pairs, comp_2: okx_pairs}
        return trade_pairs


    elif combo== 'kraken_pairs/okx_pairs':
            kraken_pairs=[]
            okx_pairs=[]

            for i_pair in pair_2[comp_2]:
                restruct=i_pair.replace('-','/')
                for j_pair in pair_1[comp_1]:
                    if restruct == j_pair:
                        kraken_pairs.append(j_pair)
                        okx_pairs.append(i_pair)
            trade_pairs= {comp_1:kraken_pairs, comp_2:okx_pairs}
            return trade_pairs


    elif combo== 'btcturk_pairs/okx_pairs':
        btcturk_pairs=[]
        okx_pairs=[]
        indexer=[]

        #itirate through btcturk pairs
        for i_pair in pair_1[comp_1]:
            #make a new list thats an indexer

            new_pair_usd=i_pair.replace('_TRY', '-USD')
            new_pair_usdt=i_pair.replace('_TRY','-USDT')
            normal_pair=i_pair
            indexer.append((new_pair_usd,new_pair_usdt,normal_pair))

        #itirate through okx pairs
        for j_pair in pair_2[comp_2]:
            for i_pair in indexer:
                if j_pair==i_pair[0] :
                    btcturk_pairs.append(i_pair[2])
                    okx_pairs.append(j_pair)
                elif j_pair==i_pair[1]:
                    btcturk_pairs.append(i_pair[2])
                    okx_pairs.append(j_pair)

        trade_pairs = {comp_1: btcturk_pairs, comp_2: okx_pairs}
        return trade_pairs


    elif combo == 'coinbase_pairs/okcoin_pairs':

        okcoin_pairs = []
        coinbase_pairs = []
        for i_pair in pair_1[comp_1]:
            for j_pair in pair_2[comp_2]:
                if i_pair == j_pair:
                    coinbase_pairs.append(i_pair)
                    okcoin_pairs.append(j_pair)
        trade_pairs = {comp_1: coinbase_pairs, comp_2: okcoin_pairs}
        return trade_pairs



    elif combo== 'kraken_pairs/okcoin_pairs':
            kraken_pairs=[]
            okcoin_pairs=[]

            for i_pair in pair_2[comp_2]:
                restruct=i_pair.replace('-','/')
                for j_pair in pair_1[comp_1]:
                    if restruct == j_pair:
                        kraken_pairs.append(j_pair)
                        okcoin_pairs.append(i_pair)
            trade_pairs= {comp_1:kraken_pairs, comp_2:okcoin_pairs}
            return trade_pairs


    elif combo=='ftx_pairs/okcoin_pairs':
        ftx_pairs= []
        okcoin_pairs=[]

        for i_pair in pair_2[comp_2]:
            restruct = i_pair.replace('-', '/')
            for j_pair in pair_1[comp_1]:
                if restruct == j_pair:
                    ftx_pairs.append(j_pair)
                    okcoin_pairs.append(i_pair)
        trade_pairs = {comp_1: ftx_pairs, comp_2: okcoin_pairs}
        return trade_pairs


    elif combo == 'okx_pairs/okcoin_pairs':
        okcoin_pairs = []
        okx_pairs = []

        for i_pair in pair_1[comp_1]:
            for j_pair in pair_2[comp_2]:
                if i_pair == j_pair:
                    okx_pairs.append(i_pair)
                    okcoin_pairs.append(j_pair)
        trade_pairs = {comp_1: okx_pairs, comp_2: okcoin_pairs}
        return trade_pairs


    elif combo == 'btcturk_pairs/okcoin_pairs':
        btcturk_pairs = []
        okcoin_pairs = []
        indexer = []

        # itirate through btcturk pairs
        for i_pair in pair_1[comp_1]:
            # make a new list thats an indexer

            new_pair_usd = i_pair.replace('_TRY', '-USD')
            new_pair_usdt = i_pair.replace('_TRY', '-USDT')
            normal_pair = i_pair
            indexer.append((new_pair_usd, new_pair_usdt, normal_pair))

        # itirate through okx pairs
        for j_pair in pair_2[comp_2]:
            for i_pair in indexer:
                if j_pair == i_pair[0]:
                    btcturk_pairs.append(i_pair[2])
                    okcoin_pairs.append(j_pair)
                elif j_pair == i_pair[1]:
                    btcturk_pairs.append(i_pair[2])
                    okcoin_pairs.append(j_pair)

        trade_pairs = {comp_1: btcturk_pairs, comp_2: okcoin_pairs}
        return trade_pairs


    elif combo=='coinbase_pairs/huobi_pairs':
        coinbase_pairs=[]
        huobi_pairs=[]
        indexer=[]
        #Reconstruct huobi pairs

        for pair in  pair_2[comp_2]:
            pair_upper= pair.upper()
            if 'HUSDT' in pair_upper:
                new_pair=pair_upper.replace('USDT','-USDT')
                indexer.append((new_pair,pair))
            elif 'HHUSD' in pair_upper:
                new_pair=pair_upper.replace('HUSD', '-USD')
                indexer.append((new_pair, pair))
            elif 'USDT' in pair_upper:
                new_pair = pair_upper.replace('USDT', '-USDT')
                indexer.append((new_pair, pair))


        #Loop through coinbase pairs

        for i_pair in pair_1[comp_1]:
            for j_pair in indexer:
                if i_pair ==j_pair[0]:
                    coinbase_pairs.append(i_pair)
                    huobi_pairs.append(j_pair[1])
        trade_pairs={comp_1:coinbase_pairs, comp_2:huobi_pairs}

        return trade_pairs


    elif combo == 'kraken_pairs/huobi_pairs':
        kraken_pairs = []
        huobi_pairs = []
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

        # Loop through coinbase pairs

        for i_pair in pair_1[comp_1]:
            for j_pair in indexer:
                if i_pair == j_pair[0]:
                    kraken_pairs.append(i_pair)
                    huobi_pairs.append(j_pair[1])
        trade_pairs = {comp_1: kraken_pairs, comp_2: huobi_pairs}

        return trade_pairs



    elif combo == 'okx_pairs/huobi_pairs':
        okx_pairs = []
        huobi_pairs = []
        indexer = []
        # Reconstruct huobi pairs

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

        # Loop through coinbase pairs

        for i_pair in pair_1[comp_1]:
            for j_pair in indexer:
                if i_pair == j_pair[0]:
                    okx_pairs.append(i_pair)
                    huobi_pairs.append(j_pair[1])
        trade_pairs = {comp_1: okx_pairs, comp_2: huobi_pairs}

        return trade_pairs


    elif combo == 'ftx_pairs/huobi_pairs':
        ftx_pairs = []
        huobi_pairs = []
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

        # Loop through coinbase pairs

        for i_pair in pair_1[comp_1]:
            for j_pair in indexer:
                if i_pair == j_pair[0]:
                    ftx_pairs.append(i_pair)
                    huobi_pairs.append(j_pair[1])
        trade_pairs = {comp_1: ftx_pairs, comp_2: huobi_pairs}

        return trade_pairs


    elif combo == 'okcoin_pairs/huobi_pairs':
        okcoin_pairs = []
        huobi_pairs = []
        indexer = []
        # Reconstruct huobi pairs

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


        # Loop through coinbase pairs

        for i_pair in pair_1[comp_1]:
            for j_pair in indexer:
                if i_pair == j_pair[0]:
                    okcoin_pairs.append(i_pair)
                    huobi_pairs.append(j_pair[1])
        trade_pairs = {comp_1: okcoin_pairs, comp_2: huobi_pairs}

        return trade_pairs


    elif combo == 'btcturk_pairs/huobi_pairs':
        btcturk_pairs = []
        huobi_pairs = []
        indexer_btcturk = []
        indexer_huobi=[]

        # itirate through btcturk pairs and reconstruct
        for i_pair in pair_1[comp_1]:
            # make a new list thats an indexer

            new_pair_usd = i_pair.replace('_TRY', '/USD')
            new_pair_usdt = i_pair.replace('_TRY', '/USDT')
            normal_pair = i_pair
            indexer_btcturk.append((new_pair_usd, new_pair_usdt, normal_pair))

            # Loop through huobi pars and reconstruct
        for pair in pair_2[comp_2]:
            pair_upper = pair.upper()
            if 'HUSDT' in pair_upper:
                new_pair = pair_upper.replace('USDT', '/USDT')
                indexer_huobi.append((new_pair, pair))
            elif 'HHUSD' in pair_upper:
                new_pair = pair_upper.replace('HUSD', '/USD')
                indexer_huobi.append((new_pair, pair))
            elif 'USDT' in pair_upper:
                new_pair = pair_upper.replace('USDT', '/USDT')
                indexer_huobi.append((new_pair, pair))

        #Find the common pairs
        for i_pair in indexer_huobi:
            for j_pair in indexer_btcturk:
                if i_pair[0]==j_pair[0]:
                    huobi_pairs.append((i_pair[0],i_pair[1]))
                    btcturk_pairs.append((j_pair[0],j_pair[2]))
                elif i_pair[0]==j_pair[1]:
                    huobi_pairs.append((i_pair[0],i_pair[1]))
                    btcturk_pairs.append((j_pair[1],j_pair[2]))

        trade_pairs={comp_1:btcturk_pairs,comp_2:huobi_pairs}
        return trade_pairs




#retreive a trade pair from the json trade pairs
def get_trade_pairs(combo):

    # Get the tradable pair dictionary according to the ask and bid exchanges
    if combo == 'btcturk_pairs/ftx_pairs' or combo == 'ftx_pairs/btcturk_pairs':
        f = open('trade_pairs_btcturk_ftx_dict.json')
    elif combo == 'btcturk_pairs/coinbase_pairs' or combo == 'coinbase_pairs/btcturk_pairs':
        f = open('trade_pairs_btcturk_coinbase_dict.json')
    elif combo == 'ftx_pairs/coinbase_pairs' or combo == 'coinbase_pairs/ftx_pairs':
        f = open('trade_pairs_ftx_coinbase_dict.json')
    elif combo == 'ftx_pairs/kraken_pairs' or combo == 'kraken_pairs/ftx_pairs':
        f = open('trade_pairs_ftx_kraken_dict.json')
    elif combo == 'btcturk_pairs/kraken_pairs' or combo == 'kraken_pairs/btcturk_pairs':
        f = open('trade_pairs_kraken_btcturk_dict.json')
    elif combo == 'coinbase_pairs/kraken_pairs' or combo == 'kraken_pairs/coinbase_pairs':
        f = open('trade_pairs_kraken_coinbase_dict.json')
    elif combo == 'btcturk_pairs/okx_pairs' or combo == 'okx_pairs/btcturk_pairs':
        f = open('trade_pairs_btcturk_okx_dict.json')
    elif combo == 'ftx_pairs/okx_pairs' or combo == 'okx_pairs/ftx_pairs':
        f = open('trade_pairs_ftx_okx_dict.json')
    elif combo == 'kraken_pairs/okx_pairs' or combo == 'okx_pairs/kraken_pairs':
        f = open('trade_pairs_kraken_okx_dict.json')
    elif combo == 'coinbase_pairs/okx_pairs' or combo == 'okx_pairs/coinbase_pairs':
        f = open('trade_pairs_coinbase_okx_dict.json')
    elif combo == 'okx_pairs/okcoin_pairs' or combo == 'okcoin_pairs/okx_pairs':
        f = open('trade_pairs_okx_okcoin_dict.json')
    elif combo == 'btcturk_pairs/okcoin_pairs' or combo == 'okcoin_pairs/btcturk_pairs':
        f = open('trade_pairs_btcturk_okcoin_dict.json')
    elif combo == 'ftx_pairs/okcoin_pairs' or combo == 'okcoin_pairs/ftx_pairs':
        f = open('trade_pairs_ftx_okcoin_dict.json')
    elif combo == 'kraken_pairs/okcoin_pairs' or combo == 'okcoin_pairs/kraken_pairs':
        f = open('trade_pairs_kraken_okcoin_dict.json')
    elif combo == 'coinbase_pairs/okcoin_pairs' or combo == 'okcoin_pairs/coinbase_pairs':
        f = open('trade_pairs_coinbase_okcoin_dict.json')
    elif combo == 'btcturk_pairs/huobi_pairs' or combo == 'huobi_pairs/btcturk_pairs':
        f = open('trade_pairs_btcturk_huobi_dict.json')
    elif combo == 'ftx_pairs/huobi_pairs' or combo == 'huobi_pairs/ftx_pairs':
        f = open('trade_pairs_ftx_huobi_dict.json')
    elif combo == 'kraken_pairs/huobi_pairs' or combo == 'huobi_pairs/kraken_pairs':
        f = open('trade_pairs_kraken_huobi_dict.json')
    elif combo == 'coinbase_pairs/huobi_pairs' or combo == 'huobi_pairs/coinbase_pairs':
        f = open('trade_pairs_coinbase_huobi_dict.json')
    elif combo == 'okx_pairs/huobi_pairs' or combo == 'huobi_pairs/okx_pairs':
        f = open('trade_pairs_okx_huobi_dict.json')
    elif combo == 'okcoin_pairs/huobi_pairs' or combo == 'huobi_pairs/okcoin_pairs':
        f = open('trade_pairs_okcoin_huobi_dict.json')
    else:
        print('Check the ask and bid exchange')
        exit()

    trade_pairs = json.load(f)
    return trade_pairs




# Create a new list for selected coins pairs NOTE İT DOESNT MATTER WHİCH ONE İS THE ASK OR BİD EXCHANGE BECAUSE WE ARE ONLY GETTİNG TİCKERS NOT PRİCES
def select_pairs(trade_pairs, pair,ask_exchange,bid_exchange):
    exchange_pairs_1 = trade_pairs[ask_exchange]
    exchange_pairs_2 = trade_pairs[bid_exchange]
    selected_exchange1_pairs = []
    selected_exchange2_pairs = []
    #Check for the coinbase/btcturk or okx/btcturk combination and change the pair from X/Y to X-Y
    combo=ask_exchange+'/'+bid_exchange

    if combo == 'coinbase_pairs/btcturk_pairs' or combo=='btcturk_pairs/coinbase_pairs' or combo=='okx_pairs/btcturk_pairs' or combo=='btcturk_pairs/okx_pairs' or combo=='coinbase_pairs/okx_pairs' or combo=='okx_pairs/coinbase_pairs' or combo == 'okcoin_pairs/btcturk_pairs' or combo == 'btcturk_pairs/okcoin_pairs'\
    or combo == 'coinbase_pairs/okcoin_pairs' or combo == 'okcoin_pairs/coinbase_pairs' or combo=='okx_pairs/okcoin_pairs' or combo=='okcoin_pairs/okx_pairs'      or combo=='coinbase_pairs/huobi_pairs' or combo=='huobi_pairs/coinbase_pairs' or combo=='okx_pairs/huobi_pairs' or combo=='huobi_pairs/okx_pairs'   or combo=='okcoin_pairs/huobi_pairs' or combo=='huobi_pairs/okcoin_pairs':
        for t_pair in pair:
            pair[pair.index(t_pair)] = t_pair.replace('/', '-')





    #Find the the trade pairs that are given from the argument
    for t_pair in pair:
        counter = 0
        while counter < len(exchange_pairs_2):
            if ask_exchange=='ftx_pairs' and bid_exchange=='btcturk_pairs' and t_pair == exchange_pairs_1[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'btcturk_pairs' and bid_exchange == 'ftx_pairs' and t_pair == exchange_pairs_2[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'ftx_pairs' and bid_exchange == 'coinbase_pairs' and t_pair == exchange_pairs_1[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'coinbase_pairs' and bid_exchange == 'ftx_pairs' and t_pair == exchange_pairs_2[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'coinbase_pairs' and bid_exchange == 'btcturk_pairs' and t_pair == exchange_pairs_1[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'btcturk_pairs' and bid_exchange == 'coinbase_pairs' and t_pair == exchange_pairs_2[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'kraken_pairs' and bid_exchange == 'ftx_pairs' and t_pair == exchange_pairs_1[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'ftx_pairs' and bid_exchange == 'kraken_pairs' and t_pair == exchange_pairs_2[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'kraken_pairs' and bid_exchange == 'btcturk_pairs' and t_pair == exchange_pairs_1[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'btcturk_pairs' and bid_exchange == 'kraken_pairs' and t_pair == exchange_pairs_2[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'kraken_pairs' and bid_exchange == 'coinbase_pairs' and t_pair == exchange_pairs_1[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'coinbase_pairs' and bid_exchange == 'kraken_pairs' and t_pair == exchange_pairs_2[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'btcturk_pairs' and bid_exchange == 'okx_pairs' and t_pair == exchange_pairs_2[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'okx_pairs' and bid_exchange == 'btcturk_pairs' and t_pair == exchange_pairs_1[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'okx_pairs' and bid_exchange == 'ftx_pairs' and t_pair == exchange_pairs_2[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'ftx_pairs' and bid_exchange == 'okx_pairs' and t_pair == exchange_pairs_1[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'okx_pairs' and bid_exchange == 'kraken_pairs' and t_pair == exchange_pairs_2[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'kraken_pairs' and bid_exchange == 'okx_pairs' and t_pair == exchange_pairs_1[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'okx_pairs' and bid_exchange == 'coinbase_pairs' and t_pair == exchange_pairs_1[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'coinbase_pairs' and bid_exchange == 'okx_pairs' and t_pair == exchange_pairs_2[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'btcturk_pairs' and bid_exchange == 'okcoin_pairs' and t_pair == exchange_pairs_2[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'okcoin_pairs' and bid_exchange == 'btcturk_pairs' and t_pair == exchange_pairs_1[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'okcoin_pairs' and bid_exchange == 'ftx_pairs' and t_pair == exchange_pairs_2[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'ftx_pairs' and bid_exchange == 'okcoin_pairs' and t_pair == exchange_pairs_1[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'okcoin_pairs' and bid_exchange == 'kraken_pairs' and t_pair == exchange_pairs_2[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'kraken_pairs' and bid_exchange == 'okcoin_pairs' and t_pair == exchange_pairs_1[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'okcoin_pairs' and bid_exchange == 'coinbase_pairs' and t_pair == exchange_pairs_1[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'coinbase_pairs' and bid_exchange == 'okcoin_pairs' and t_pair == exchange_pairs_2[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'okcoin_pairs' and bid_exchange == 'okx_pairs' and t_pair == exchange_pairs_1[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'okx_pairs' and bid_exchange == 'okcoin_pairs' and t_pair == exchange_pairs_2[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])


            elif ask_exchange == 'coinbase_pairs' and bid_exchange == 'huobi_pairs' and t_pair == exchange_pairs_1[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'huobi_pairs' and bid_exchange == 'coinbase_pairs' and t_pair == exchange_pairs_2[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'kraken_pairs' and bid_exchange == 'huobi_pairs' and t_pair == exchange_pairs_1[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'huobi_pairs' and bid_exchange == 'kraken_pairs' and t_pair == exchange_pairs_2[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'okx_pairs' and bid_exchange == 'huobi_pairs' and t_pair == exchange_pairs_1[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'huobi_pairs' and bid_exchange == 'okx_pairs' and t_pair == exchange_pairs_2[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'ftx_pairs' and bid_exchange == 'huobi_pairs' and t_pair == exchange_pairs_1[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'huobi_pairs' and bid_exchange == 'ftx_pairs' and t_pair == exchange_pairs_2[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'okcoin_pairs' and bid_exchange == 'huobi_pairs' and t_pair == exchange_pairs_1[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'huobi_pairs' and bid_exchange == 'okcoin_pairs' and t_pair == exchange_pairs_2[counter]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter])
                selected_exchange1_pairs.append(exchange_pairs_1[counter])

            elif ask_exchange == 'btcturk_pairs' and bid_exchange == 'huobi_pairs' and t_pair == exchange_pairs_1[counter][0]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter][1])
                selected_exchange1_pairs.append(exchange_pairs_1[counter][1])

            elif ask_exchange == 'huobi_pairs' and bid_exchange == 'btcturk_pairs' and t_pair == exchange_pairs_1[counter][0]:
                selected_exchange2_pairs.append(exchange_pairs_2[counter][1])
                selected_exchange1_pairs.append(exchange_pairs_1[counter][1])


            counter += 1

    selected_trade_pairs = {bid_exchange: selected_exchange2_pairs, ask_exchange: selected_exchange1_pairs}

    return selected_trade_pairs





# Form a dictionary of bid an ask prices for the selected pairs on both exchanges
def sort_price( selected_trade_pairs,bid_exchange,ask_exchange):
    btcturk_price_list = []
    ftx_price_list = []
    coinbase_price_list= []
    kraken_price_list =[]
    okx_prices_list=[]
    okcoin_prices_list=[]
    huobi_prices_list=[]
    price_dict = {}



    if bid_exchange== 'btcturk_pairs' or ask_exchange=='btcturk_pairs':
        btcturk_market = get_ticker(btcturk_url)

        # Get the bid and ask prices for each pair from BTCTurk
        for t_pair in selected_trade_pairs['btcturk_pairs']:
            for pair in btcturk_market["data"]:
                if t_pair == pair['pairNormalized']:
                    bid = float(pair['bid'])
                    ask = float(pair['ask'])
                    prices =  {'bid': bid, 'ask': ask}
                    btcturk_price_list.append(prices)

        price_dict.update({'btcturk_pairs': btcturk_price_list})


    if bid_exchange == 'ftx_pairs' or ask_exchange == 'ftx_pairs':


        # Get the bid and ask prices for each pair from FTX
        for t_pair in selected_trade_pairs['ftx_pairs']:
            ticker_prices=get_ticker(f'https://ftx.com/api/markets/{t_pair}')
            bid= float(ticker_prices["result"]['bid'])
            ask= float(ticker_prices["result"]['ask'])
            prices = {'bid': bid, 'ask': ask}
            ftx_price_list.append(prices)
        price_dict.update({'ftx_pairs': ftx_price_list})



    #Get the bid and ask price for every pair from coinbase
    if bid_exchange=='coinbase_pairs' or ask_exchange=='coinbase_pairs':

        api_key = 'gTFsLnZLFS80OXTb'
        api_secret = 'bLUG1Ao9pPF1jG0emKD30zeKdketJqKK'
        client = Client(api_key, api_secret)

        for t_pair in selected_trade_pairs['coinbase_pairs']:

            currency_code = t_pair
            ask = client.get_buy_price(currency_pair=currency_code)['amount']
            bid = client.get_sell_price(currency_pair=currency_code)['amount']
            prices = {'bid': bid, 'ask': ask}
            coinbase_price_list.append(prices)

        price_dict.update({'coinbase_pairs':coinbase_price_list})


    if bid_exchange=='kraken_pairs' or ask_exchange=='kraken_pairs':
        api = krakenex.API()
        k = KrakenAPI(api)

        for t_pair in selected_trade_pairs['kraken_pairs']:

            data = k.get_ticker_information(t_pair)
            ask= float(data['a'][0][0])
            bid= float(data['b'][0][0])
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
            ticker_prices = get_ticker(f'https://www.okcoin.com/api/spot/v3/instruments/{t_pair}/ticker')
            ask = float(ticker_prices["best_ask"])
            bid = float(ticker_prices["best_bid"])
            prices = {'bid': bid, 'ask': ask}
            okcoin_prices_list.append(prices)
        price_dict.update({'okcoin_pairs': okcoin_prices_list})


    if bid_exchange=='huobi_pairs' or ask_exchange =='huobi_pairs':

        for t_pair in selected_trade_pairs['huobi_pairs']:
            ticker_prices= get_ticker(f'https://api.huobi.pro/market/detail/merged?symbol={t_pair}')
            ask= float(ticker_prices['tick']['ask'][0])
            bid= float(ticker_prices['tick']['bid'][0])
            prices = {'bid': bid, 'ask': ask}
            huobi_prices_list.append(prices)
        price_dict.update({'huobi_pairs': huobi_prices_list})


    return price_dict





# Calculate the surface rate accoridng to scenario 1 and 2
def calc_surf_rate(price_dict, selected_trade_pairs, ask_exchange,bid_exchange,pair):

    combo = ask_exchange + '/' + bid_exchange
    # IMPORTANT : check the quote currency to see which livrate to get

    if combo == 'coinbase_pairs/btcturk_pairs' or combo == 'btcturk_pairs/coinbase_pairs' or combo == 'okx_pairs/btcturk_pairs' or combo == 'btcturk_pairs/okx_pairs' or combo == 'coinbase_pairs/okx_pairs' or combo == 'okx_pairs/coinbase_pairs' or combo == 'okcoin_pairs/btcturk_pairs' or combo == 'btcturk_pairs/okcoin_pairs' or combo == 'coinbase_pairs/okcoin_pairs' or combo == 'okcoin_pairs/coinbase_pairs' or combo == 'okx_pairs/okcoin_pairs' or combo == 'okcoin_pairs/okx_pairs' or combo == 'coinbase_pairs/huobi_pairs' or combo == 'huobi_pairs/coinbase_pairs' or combo == 'okx_pairs/huobi_pairs' or combo == 'huobi_pairs/okx_pairs' or combo == 'okcoin_pairs/huobi_pairs' or combo == 'huobi_pairs/okcoin_pairs':
        quote_check = pair[0].split('-')
    else:
        quote_check = pair[0].split('/')




    if ask_exchange=='btcturk_pairs' or bid_exchange=='btcturk_pairs':
        if quote_check[1]=='USD':
            alpha_rates_market = get_ticker(alpha_rates_usd_url)
            liverate_tickers = get_alpha_rate(alpha_rates_market)
            liverate_bid = float(liverate_tickers['bid'])
            liverate_ask = float(liverate_tickers['ask'])
        elif quote_check[1]=='USDT':
            alpha_rates_market = get_ticker(alpha_rates_usdt_url)
            liverate_tickers = get_alpha_rate(alpha_rates_market)
            liverate_bid = float(liverate_tickers['bid'])
            liverate_ask = float(liverate_tickers['ask'])
        elif quote_check[1]=='USDC':
            alpha_rates_market = get_ticker(alpha_rates_usdc_url)
            liverate_tickers = get_alpha_rate(alpha_rates_market)
            liverate_bid = float(liverate_tickers['bid'])
            liverate_ask = float(liverate_tickers['ask'])


    counter = 0
    surf_rate_list = []
    ask_price_list=price_dict[ask_exchange]
    bid_price_list = price_dict[bid_exchange]


    while counter < len(ask_price_list):

        #ask_price_list_bid = float(ask_price_list[counter]['bid'])
        ask_price_list_ask = float(ask_price_list[counter]['ask'])
        bid_price_list_bid = float(bid_price_list[counter]['bid'])
        #bid_price_list_ask = float(bid_price_list[counter]['ask'])

        if ask_exchange =='btcturk_pairs' or  bid_exchange =='btcturk_pairs':

            #Scenario 1
            btcturk_bid_usd_eqv = bid_price_list_bid / liverate_ask
            #Scenario 2
            btcturk_ask_usd_eqv = ask_price_list_ask / liverate_bid


            # Scenario 1: Buy low in foreign exchange , sell high in BTCTurk
            if btcturk_bid_usd_eqv > ask_price_list_ask and bid_exchange == 'btcturk_pairs':
                # profit = btcturk_bid_usd_eqv - ftx_ask
                # profit_perc = (profit / ftx_ask) * 100
                ask_exchange_pair = selected_trade_pairs[ask_exchange][counter]
                btcturk_pairs = selected_trade_pairs['btcturk_pairs'][counter]
                stats = {ask_exchange: ask_exchange_pair, 'btcturk_pairs': btcturk_pairs}
                surf_rate_list.append(stats)


            # Scenario 2 : Buy low in BTCTurk , sell high on foreign exchange
            elif btcturk_ask_usd_eqv < bid_price_list_bid and ask_exchange == 'btcturk_pairs':
                # profit = ftx_bid- btcturk_ask_usd_eqv
                # profit_perc = (profit / btcturk_ask_usd_eqv) * 100
                bid_exchange_pair = selected_trade_pairs[bid_exchange][counter]
                btcturk_pairs = selected_trade_pairs['btcturk_pairs'][counter]
                stats = {bid_exchange: bid_exchange_pair, 'btcturk_pairs': btcturk_pairs}
                surf_rate_list.append(stats)



        #When none of the exchanges are Turkish
        elif ask_exchange != 'btcturk_pairs' and bid_exchange != 'btcturk_pairs' and  ask_price_list_ask< bid_price_list_bid :
            bid_exchange_pairs = selected_trade_pairs[bid_exchange][counter]
            ask_exchange_pairs = selected_trade_pairs[ask_exchange][counter]
            stats = {ask_exchange: ask_exchange_pairs, bid_exchange: bid_exchange_pairs}
            surf_rate_list.append(stats)

        counter += 1

    return surf_rate_list





# Retrieve the orderbook for each pair in the list
def get_orderbook(surface_rate_list, ask_exchange, bid_exchange):

    arb_orderbook={}
    ftx_orderbook = []
    btcturk_orderbook = []
    coinbase_orderbook=[]
    kraken_orderbook=[]
    okx_orderbook=[]
    okcoin_orderbook=[]
    huobi_orderbook=[]



    # Get the orderbook for each pair in each exchange

    try:

        if ask_exchange == 'ftx_pairs' or bid_exchange == 'ftx_pairs':

            for pair in surface_rate_list:
                ftx_pair = pair['ftx_pairs']
                ftx_url = f'https://ftx.com/api/markets/{ftx_pair}/orderbook?depth=100'
                book = get_ticker(ftx_url)
                ftx_orderbook.append([ftx_pair, book])
            arb_orderbook.update({'ftx_orderbook': ftx_orderbook})

        if ask_exchange == 'btcturk_pairs' or bid_exchange == 'btcturk_pairs':

            for pair in surface_rate_list:
                btcturk_pair = pair['btcturk_pairs']
                btcturk_url = f'https://api.btcturk.com/api/v2/orderbook?pairSymbol={btcturk_pair}&limit=100'
                book = get_ticker(btcturk_url)
                btcturk_orderbook.append([btcturk_pair, book])
            arb_orderbook.update({'btcturk_orderbook': btcturk_orderbook})

        if ask_exchange == 'coinbase_pairs' or bid_exchange == 'coinbase_pairs':

            for pair in surface_rate_list:
                coinbase_pair = pair['coinbase_pairs']
                coinbase_url = f'https://api.exchange.coinbase.com/products/{coinbase_pair}/book?level=2'
                raw_book = get_ticker(coinbase_url)
                # Recontruct the book for first 100 entries
                bids = raw_book['bids'][0:100]
                asks = raw_book['asks'][0:100]
                book = {'bids': bids, 'asks': asks}
                coinbase_orderbook.append([coinbase_pair, book])
            arb_orderbook.update({'coinbase_orderbook': coinbase_orderbook})

        if ask_exchange == 'kraken_pairs' or bid_exchange == 'kraken_pairs':
            api = krakenex.API()
            k = KrakenAPI(api)

            for pair in surface_rate_list:
                kraken_pair = pair['kraken_pairs']
                data = k.get_order_book(kraken_pair, count=100)
                bid_prices = data[0]['price']
                bid_volumes = data[0]['volume']

                ask_prices = data[1]['price']
                ask_volumes = data[1]['volume']

                bid_zipped = zip(bid_prices, bid_volumes)
                ask_zipped = zip(ask_prices, ask_volumes)

                bids = list(bid_zipped)
                asks = list(ask_zipped)
                book = {'bids': bids, 'asks': asks}
                kraken_orderbook.append([kraken_pair, book])
            arb_orderbook.update({'kraken_orderbook': kraken_orderbook})

        if ask_exchange == 'okx_pairs' or bid_exchange == 'okx_pairs':

            for t_pair in surface_rate_list:
                okx_pair = t_pair['okx_pairs']
                book = get_ticker(f'https://www.okx.com/api/v5/market/books?instId={okx_pair}&sz=100')['data'][0]
                okx_orderbook.append([okx_pair, book])
            arb_orderbook.update({'okx_orderbook': okx_orderbook})

        if ask_exchange == 'okcoin_pairs' or bid_exchange == 'okcoin_pairs':

            for t_pair in surface_rate_list:
                okcoin_pair = t_pair['okcoin_pairs']
                book=get_ticker(f'https://www.okcoin.com/api/spot/v3/instruments/{okcoin_pair}/book?size=100&depth=0')
                okcoin_orderbook.append([okcoin_pair, book])
            arb_orderbook.update({'okcoin_orderbook': okcoin_orderbook})

        if ask_exchange=='huobi_pairs' or bid_exchange=='huobi_pairs':

            for t_pair in surface_rate_list:
                huobi_pair = t_pair['huobi_pairs']
                raw_orderbook = get_ticker(f'https://api.huobi.pro/market/depth?symbol={huobi_pair}&type=step0')
                bids = raw_orderbook['tick']['bids'][0:100]
                asks = raw_orderbook['tick']['asks'][0:100]
                book={'bids':bids, 'asks':asks}
                huobi_orderbook.append([huobi_pair,book])
            arb_orderbook.update({'huobi_orderbook':huobi_orderbook})



        return arb_orderbook

    except IndexError:
        print('This trade pair is not available on OKX')






# Calculate order book depth
def calc_depth(arb_orderbook,ask_exchange,bid_exchange, pair):

    combo = ask_exchange + '/' + bid_exchange

    # IMPORTANT : check the quote currency to see which livrate to get
    if combo == 'coinbase_pairs/btcturk_pairs' or combo == 'btcturk_pairs/coinbase_pairs' or combo == 'okx_pairs/btcturk_pairs' or combo == 'btcturk_pairs/okx_pairs' or combo == 'coinbase_pairs/okx_pairs' or combo == 'okx_pairs/coinbase_pairs' or combo == 'okcoin_pairs/btcturk_pairs' or combo == 'btcturk_pairs/okcoin_pairs' or combo == 'coinbase_pairs/okcoin_pairs' or combo == 'okcoin_pairs/coinbase_pairs' or combo == 'okx_pairs/okcoin_pairs' or combo == 'okcoin_pairs/okx_pairs' or combo == 'coinbase_pairs/huobi_pairs' or combo == 'huobi_pairs/coinbase_pairs' or combo == 'okx_pairs/huobi_pairs' or combo == 'huobi_pairs/okx_pairs' or combo == 'okcoin_pairs/huobi_pairs' or combo == 'huobi_pairs/okcoin_pairs':
        quote_check = pair[0].split('-')
    else:
        quote_check=pair[0].split('/')


    if ask_exchange == 'btcturk_pairs' or bid_exchange == 'btcturk_pairs':
        btcturk_orderbook = arb_orderbook['btcturk_orderbook']
        if quote_check[1] == 'USD':
            alpha_rates_market = get_ticker(alpha_rates_usd_url)
            liverate_tickers = get_alpha_rate(alpha_rates_market)
            liverate_bid = float(liverate_tickers['bid'])
            liverate_ask = float(liverate_tickers['ask'])

        elif quote_check[1] == 'USDT':
            alpha_rates_market = get_ticker(alpha_rates_usdt_url)
            liverate_tickers = get_alpha_rate(alpha_rates_market)
            liverate_bid = float(liverate_tickers['bid'])
            liverate_ask = float(liverate_tickers['ask'])

        elif quote_check[1] == 'USDC':
            alpha_rates_market = get_ticker(alpha_rates_usdc_url)
            liverate_tickers = get_alpha_rate(alpha_rates_market)
            liverate_bid = float(liverate_tickers['bid'])
            liverate_ask = float(liverate_tickers['ask'])


    if ask_exchange=='ftx_pairs' or bid_exchange== 'ftx_pairs':
        ftx_orderbook = arb_orderbook['ftx_orderbook']


    if ask_exchange == 'coinbase_pairs' or bid_exchange == 'coinbase_pairs':
        coinbase_orderbook=arb_orderbook['coinbase_orderbook']

    if ask_exchange=='kraken_pairs' or bid_exchange=='kraken_pairs':
        kraken_orderbook= arb_orderbook['kraken_orderbook']

    if ask_exchange=='okx_pairs' or bid_exchange=='okx_pairs':
        okx_orderbook=arb_orderbook['okx_orderbook']

    if ask_exchange == 'okcoin_pairs' or bid_exchange == 'okcoin_pairs':
        okcoin_orderbook = arb_orderbook['okcoin_orderbook']

    if ask_exchange == 'huobi_pairs' or bid_exchange == 'huobi_pairs':
        huobi_orderbook = arb_orderbook['huobi_orderbook']


    counter = 0
    depth_rate_list = []
    orderbook_ref= ask_exchange.replace('pairs','orderbook')

    # Loop through the orderbook
    while counter < len(arb_orderbook[orderbook_ref]):


        # Get pair name
        pair_name =  arb_orderbook[orderbook_ref][counter][0]
        # Set the orderbook
        orderbook = []

        '''BTCturk and FTX'''

        #Scenario 1 ask= ftx/bid= btcturk
        if combo=='ftx_pairs/btcturk_pairs':
            # Get the ask prices /// returns an array of arrays
            ask_prices = ftx_orderbook[counter][1]['result']['asks']
            # Get the bid prices ///returns an array of arrays
            bid_prices = btcturk_orderbook[counter][1]['data']['bids']
            # Get the USD equivalant of the prices on BTCTurk
            bid_usd_eqv_list = []
            for price in bid_prices:
                bid_usd_eqv = float(price[0]) / liverate_ask
                bid_usd_eqv_list.append(bid_usd_eqv)


        # Scenario 2 ask= btcturk/bid= ftx
        elif combo=='btcturk_pairs/ftx_pairs':
            # Get the bid prices ///returns an array of arrays
            bid_prices = ftx_orderbook[counter][1]['result']['bids']
            # Get the ask prices /// returns an array of arrays
            ask_prices = btcturk_orderbook[counter][1]['data']['asks']
            ask_usd_eqv_list = []
            for price in ask_prices:
                ask_usd_eqv = float(price[0]) / liverate_bid
                ask_usd_eqv_list.append(ask_usd_eqv)

            ''' Coinbase and BTCturk'''

        #Scenario 3 ask=btcturk/bid= coinbase
        elif combo=='btcturk_pairs/coinbase_pairs':
            #Returns an array of arrays
            bid_prices=coinbase_orderbook[counter][1]['bids']
            ask_prices = btcturk_orderbook[counter][1]['data']['asks']
            ask_usd_eqv_list = []
            for price in ask_prices:
                ask_usd_eqv = float(price[0]) / liverate_bid
                ask_usd_eqv_list.append(ask_usd_eqv)


        #Scenario 4 ask= coinbase/ bid = btcturk
        elif combo=='coinbase_pairs/btcturk_pairs':
            # Returns an array of arrays
            ask_prices=coinbase_orderbook[counter][1]['asks']
            bid_prices = btcturk_orderbook[counter][1]['data']['bids']
            # Get the USD equivalant of the prices on BTCTurk
            bid_usd_eqv_list = []
            for price in bid_prices:
                bid_usd_eqv = float(price[0]) / liverate_ask
                bid_usd_eqv_list.append(bid_usd_eqv)


            ''''Conibase and FTX'''
          #Scenario 5 ask=coinbase/bid=ftx
        elif combo=='coinbase_pairs/ftx_pairs':
            # Returns an array of arrays
            ask_prices = coinbase_orderbook[counter][1]['asks']
            # Get the bid prices ///returns an array of arrays
            bid_prices = ftx_orderbook[counter][1]['result']['bids']

            #Scenario 6 ask= ftx/bid = coinbase

        elif combo=='ftx_pairs/coinbase_pairs':
            # Get the ask prices /// returns an array of arrays
            ask_prices = ftx_orderbook[counter][1]['result']['asks']
            # Get the bid prices /// returns an array of arrays
            bid_prices = coinbase_orderbook[counter][1]['bids']




            '''FTX and Kraken'''
        # Scenario 7 ask=ftx/bid= kraken
        elif combo=='ftx_pairs/kraken_pairs':

            # Get the ask prices /// returns an array of arrays
            ask_prices = ftx_orderbook[counter][1]['result']['asks']
            # Get the bid prices /// returns an array of arrays
            bid_prices = kraken_orderbook[counter][1]['bids']


        # Scenario 8 ask=kraken/bid= ftx
        elif combo == 'kraken_pairs/ftx_pairs':

            # Get the ask prices /// returns an array of arrays
            ask_prices = kraken_orderbook[counter][1]['asks']
            # Get the bid prices /// returns an array of arrays
            bid_prices = ftx_orderbook[counter][1]['result']['bids']


            '''BTCturk and Kraken'''
         #Scenario 9 ask= kraken/bid= btcturk
        elif combo=='kraken_pairs/btcturk_pairs':
            # Get the ask prices /// returns an array of arrays
            ask_prices = kraken_orderbook[counter][1]['asks']
            # Get the bid prices ///returns an array of arrays
            bid_prices = btcturk_orderbook[counter][1]['data']['bids']
            # Get the USD equivalant of the prices on BTCTurk
            bid_usd_eqv_list = []
            for price in bid_prices:
                bid_usd_eqv = float(price[0]) / liverate_ask
                bid_usd_eqv_list.append(bid_usd_eqv)

        #Scenario 10 ask= btcturk/bid= kraken
        elif combo=='btcturk_pairs/kraken_pairs':
            # Get the bid prices /// returns an array of arrays
            bid_prices = kraken_orderbook[counter][1]['bids']
            ask_prices = btcturk_orderbook[counter][1]['data']['asks']
            ask_usd_eqv_list = []
            for price in ask_prices:
                ask_usd_eqv = float(price[0]) / liverate_bid
                ask_usd_eqv_list.append(ask_usd_eqv)



                '''Kraken and Coinbase'''


         #Scenario 11 ask= kraken/bid=coinbase
        elif combo=='kraken_pairs/coinbase_pairs':
            # Get the ask prices /// returns an array of arrays
            ask_prices = kraken_orderbook[counter][1]['asks']
            # Get the bid prices /// returns an array of arrays
            bid_prices = coinbase_orderbook[counter][1]['bids']


        # Scenario 12 ask= coinbase/bid=kraken
        elif combo == 'coinbase_pairs/kraken_pairs':
            # Returns an array of arrays
            ask_prices = coinbase_orderbook[counter][1]['asks']
            # Get the bid prices /// returns an array of arrays
            bid_prices = kraken_orderbook[counter][1]['bids']


            '''Coinbase and OKX'''


        #Scenario 13 ask= coinbase /bid = okx
        elif combo =='coinbase_pairs/okx_pairs':
            # Returns an array of arrays
            ask_prices = coinbase_orderbook[counter][1]['asks']
            bid_prices= okx_orderbook[counter][1]['bids']

        # Scenario 14 ask= okx /bid = coinbase
        elif combo == 'okx_pairs/coinbase_pairs':
            # Returns an array of arrays
            bid_prices = coinbase_orderbook[counter][1]['bids']
            ask_prices = okx_orderbook[counter][1]['asks']



            '''Kraken and OKX'''


        #Scenario 15 ask=krkaen/bid= okx
        elif combo=='kraken_pairs/okx_pairs':
            # Get the ask prices /// returns an array of arrays
            ask_prices = kraken_orderbook[counter][1]['asks']
            bid_prices = okx_orderbook[counter][1]['bids']

        #Scenario 16 ask= okx/ bid= kraken
        elif combo == 'okx_pairs/kraken_pairs':
            # Get the ask prices /// returns an array of arrays
            bid_prices = kraken_orderbook[counter][1]['bids']
            ask_prices = okx_orderbook[counter][1]['asks']



            '''FTX and OKX'''

        #Scenario 17 ask= ftx/bid= okx
        elif combo == 'ftx_pairs/okx_pairs':
            # Get the ask prices /// returns an array of arrays
            ask_prices = ftx_orderbook[counter][1]['result']['asks']
            bid_prices = okx_orderbook[counter][1]['bids']

            # Scenario 18 ask= OKX/bid= FTX

        elif combo == 'okx_pairs/ftx_pairs':
            # Get the ask prices /// returns an array of arrays
            bid_prices = ftx_orderbook[counter][1]['result']['bids']
            ask_prices = okx_orderbook[counter][1]['asks']


            '''BTCturk and OKX'''


        #Scenario 19 ask=btcturk/bid= okx
        elif combo=='btcturk_pairs/okx_pairs':
            bid_prices = okx_orderbook[counter][1]['bids']
            ask_prices = btcturk_orderbook[counter][1]['data']['asks']
            ask_usd_eqv_list = []
            for price in ask_prices:
                ask_usd_eqv = float(price[0]) / liverate_bid
                ask_usd_eqv_list.append(ask_usd_eqv)


        # Scenario 20 ask=okx/bid= btcturk
        elif combo == 'okx_pairs/btcturk_pairs':
            ask_prices = okx_orderbook[counter][1]['asks']
            bid_prices = btcturk_orderbook[counter][1]['data']['bids']
            # Get the USD equivalant of the prices on BTCTurk
            bid_usd_eqv_list = []
            for price in bid_prices:
                bid_usd_eqv = float(price[0]) / liverate_ask
                bid_usd_eqv_list.append(bid_usd_eqv)

            '''Coinbase and OKcoin'''
        # Scenario 21 ask= coinbase /bid = okcoin
        elif combo == 'coinbase_pairs/okcoin_pairs':
            # Returns an array of arrays
            ask_prices = coinbase_orderbook[counter][1]['asks']
            bid_prices = okcoin_orderbook[counter][1]['bids']

        # Scenario 22 ask= okcoin /bid = coinbase
        elif combo == 'okcoin_pairs/coinbase_pairs':
            # Returns an array of arrays
            bid_prices = coinbase_orderbook[counter][1]['bids']
            ask_prices = okcoin_orderbook[counter][1]['asks']

            '''Kraken and OKcoin'''

        # Scenario 23 ask=krkaen/bid= okcoin
        elif combo == 'kraken_pairs/okcoin_pairs':
            # Get the ask prices /// returns an array of arrays
            ask_prices = kraken_orderbook[counter][1]['asks']
            bid_prices = okcoin_orderbook[counter][1]['bids']

        # Scenario 24 ask= okcoin/ bid= kraken
        elif combo == 'okcoin_pairs/kraken_pairs':
            # Get the ask prices /// returns an array of arrays
            bid_prices = kraken_orderbook[counter][1]['bids']
            ask_prices = okcoin_orderbook[counter][1]['asks']

            '''FTX and OKcoin'''


        # Scenario 25 ask= ftx/bid= okcoin
        elif combo == 'ftx_pairs/okcoin_pairs':
            # Get the ask prices /// returns an array of arrays
            ask_prices = ftx_orderbook[counter][1]['result']['asks']
            bid_prices = okcoin_orderbook[counter][1]['bids']

         # Scenario 26 ask= OKcoin/bid= FTX
        elif combo == 'okcoin_pairs/ftx_pairs':
            # Get the ask prices /// returns an array of arrays
            bid_prices = ftx_orderbook[counter][1]['result']['bids']
            ask_prices = okcoin_orderbook[counter][1]['asks']

            '''BTCturk and OKcoin'''


        # Scenario 27 ask=btcturk/bid= okcoin
        elif combo == 'btcturk_pairs/okcoin_pairs':
            bid_prices = okcoin_orderbook[counter][1]['bids']
            ask_prices = btcturk_orderbook[counter][1]['data']['asks']
            ask_usd_eqv_list = []
            for price in ask_prices:
                ask_usd_eqv = float(price[0]) / liverate_bid
                ask_usd_eqv_list.append(ask_usd_eqv)

        # Scenario 28 ask=okcoin/bid= btcturk
        elif combo == 'okcoin_pairs/btcturk_pairs':
            ask_prices = okcoin_orderbook[counter][1]['asks']
            bid_prices = btcturk_orderbook[counter][1]['data']['bids']
            # Get the USD equivalant of the prices on BTCTurk
            bid_usd_eqv_list = []
            for price in bid_prices:
                bid_usd_eqv = float(price[0]) / liverate_ask
                bid_usd_eqv_list.append(bid_usd_eqv)

            '''OKX and OKcoin'''


        # Scenario 29 ask= okx /bid = okcoin
        elif combo == 'okx_pairs/okcoin_pairs':
            # Returns an array of arrays
            ask_prices = okx_orderbook[counter][1]['asks']
            bid_prices = okcoin_orderbook[counter][1]['bids']

        # Scenario 30 ask= okcoin /bid = okx
        elif combo == 'okcoin_pairs/okx_pairs':
            # Returns an array of arrays
            bid_prices = okx_orderbook[counter][1]['bids']
            ask_prices = okcoin_orderbook[counter][1]['asks']


            '''Coinbase and huobi'''


        elif combo== 'coinbase_pairs/huobi_pairs':
            ask_prices = coinbase_orderbook[counter][1]['asks']
            bid_prices=huobi_orderbook[counter][1]['bids']

        elif combo== 'huobi_pairs/coinbase_pairs':
            ask_prices = huobi_orderbook[counter][1]['asks']
            bid_prices=coinbase_orderbook[counter][1]['bids']


            '''Kraken and huobi'''
        elif combo=='kraken_pairs/huobi_pairs':
            ask_prices = kraken_orderbook[counter][1]['asks']
            bid_prices = huobi_orderbook[counter][1]['bids']

        elif combo=='huobi_pairs/kraken_pairs':
            ask_prices = huobi_orderbook[counter][1]['asks']
            bid_prices = kraken_orderbook[counter][1]['bids']


            '''OKX and huobi'''

        elif combo=='okx_pairs/huobi_pairs':
            ask_prices = okx_orderbook[counter][1]['asks']
            bid_prices = huobi_orderbook[counter][1]['bids']

        elif combo == 'huobi_pairs/okx_pairs':
            ask_prices = huobi_orderbook[counter][1]['asks']
            bid_prices = okx_orderbook[counter][1]['bids']

            '''FTX amd huobi'''


        elif combo=='ftx_pairs/huobi_pairs':
            ask_prices = ftx_orderbook[counter][1]['result']['asks']
            bid_prices = huobi_orderbook[counter][1]['bids']

        elif combo == 'huobi_pairs/ftx_pairs':
            ask_prices = huobi_orderbook[counter][1]['asks']
            bid_prices = ftx_orderbook[counter][1]['result']['bids']


            '''Okcoin and huobi'''


        elif combo == 'okcoin_pairs/huobi_pairs':
            ask_prices = okcoin_orderbook[counter][1]['asks']
            bid_prices = huobi_orderbook[counter][1]['bids']

        elif combo == 'huobi_pairs/okcoin_pairs':
            ask_prices = huobi_orderbook[counter][1]['asks']
            bid_prices = okcoin_orderbook[counter][1]['bids']


            ''' BTCturk and huobi'''

        elif combo=='btcturk_pairs/huobi_pairs':
            bid_prices = huobi_orderbook[counter][1]['bids']
            ask_prices = btcturk_orderbook[counter][1]['data']['asks']
            ask_usd_eqv_list = []
            for price in ask_prices:
                ask_usd_eqv = float(price[0]) / liverate_bid
                ask_usd_eqv_list.append(ask_usd_eqv)

        elif combo=='huobi_pairs/btcturk_pairs':
            ask_prices = huobi_orderbook[counter][1]['asks']
            bid_prices = btcturk_orderbook[counter][1]['data']['bids']
            # Get the USD equivalant of the prices on BTCTurk
            bid_usd_eqv_list = []
            for price in bid_prices:
                bid_usd_eqv = float(price[0]) / liverate_ask
                bid_usd_eqv_list.append(bid_usd_eqv)




        price_counter = 0
        while price_counter < len(bid_prices):

            if bid_exchange=='btcturk_pairs':
                bid_TRY = bid_prices[price_counter][0]
                bid_usd_eqvl = bid_usd_eqv_list[price_counter]
                ask = float(ask_prices[price_counter][0])
                profit = bid_usd_eqvl - ask
                profit_perc = (profit / ask) * 100


            elif ask_exchange=='btcturk_pairs':
                ask_TRY = ask_prices[price_counter][0]
                ask_usd_eqvl = ask_usd_eqv_list[price_counter]
                bid = float(bid_prices[price_counter][0])
                profit = bid-ask_usd_eqvl
                profit_perc = (profit / ask_usd_eqvl) * 100


            #Both foreign exchanges
            elif 'btcturk' not in combo:
                ask = float(ask_prices[price_counter][0])
                bid = float(bid_prices[price_counter][0])
                profit= bid-ask
                profit_perc=(profit/ask)* 100


            if float(bid_prices[price_counter][1]) > float(ask_prices[price_counter][1]):
                vol = float(ask_prices[price_counter][1])
            else:
                vol = float(bid_prices[price_counter][1])

            # Check for minimum profit
            if profit_perc >= 0.000001 and bid_exchange=='btcturk_pairs':
                orderbook.append((ask, f'{bid_TRY} ({round(bid_usd_eqvl,1)})', vol, profit_perc))

            elif profit_perc >= 0.000001 and ask_exchange == 'btcturk_pairs':
                orderbook.append((f'{ask_TRY} ({round(ask_usd_eqvl,1)})',bid, vol, profit_perc))

            elif profit_perc >= 0.000001 and 'btcturk' not in combo:
                orderbook.append((ask, bid, vol, profit_perc))


            price_counter += 1

        #print('orderbook ',orderbook)

        total_vol_1 = 0
        weighted_sum_1 = 0

        total_vol_2 = 0
        weighted_sum_2 = 0

        total_vol_3 = 0
        weighted_sum_3 = 0

        total_vol_4 = 0
        weighted_sum_4 = 0

        total_vol_5 = 0
        weighted_sum_5 = 0

        total_vol_6 = 0
        weighted_sum_6 = 0

        ask_1 = None
        ask_2 = None
        ask_3 = None
        ask_4 = None
        ask_5 = None
        ask_6 = None


        bid_1 = None
        bid_2 = None
        bid_3 = None
        bid_4 = None
        bid_5 = None
        bid_6 = None

        vol_1 = None
        vol_2 = None
        vol_3 = None
        vol_4 = None
        vol_5 = None
        vol_6 = None

        for element in orderbook:

            ask = element[0]
            bid = element[1]
            vol = element[2]
            profit_perc = element[3]

            # For a profit of >=1 %
            if profit_perc >= 1:
                total_vol_1 += vol
                weighted_sum_1 += vol * profit_perc
                ask_1 = ask
                bid_1 = bid
                vol_1 = vol

            # For a profit of >=0.75 %
            if profit_perc >= 0.75:
                total_vol_2 += vol
                weighted_sum_2 += vol * profit_perc
                ask_2 = ask
                bid_2 = bid
                vol_2 = vol

            # For a profit of >=0.5 %
            if profit_perc >= 0.5:
                total_vol_3 += vol
                weighted_sum_3 += vol * profit_perc
                ask_3 = ask
                bid_3 = bid
                vol_3 = vol

            # For a profit of >=0.25 %
            if profit_perc >= 0.25:
                total_vol_4 += vol
                weighted_sum_4 += vol * profit_perc
                ask_4 = ask
                bid_4 = bid
                vol_4 = vol

            # For a profit of >=0.1 %
            if profit_perc >= 0.1:
                total_vol_5 += vol
                weighted_sum_5 += vol * profit_perc
                ask_5 = ask
                bid_5 = bid
                vol_5 = vol

            # For a profit of >=0.1 %
            if profit_perc >= 0.01:
                total_vol_6 += vol
                weighted_sum_6 += vol * profit_perc
                ask_6 = ask
                bid_6 = bid
                vol_6 = vol

        if total_vol_1 != 0:
            average_1 = weighted_sum_1 / total_vol_1
        else:
            average_1 = 0

        if total_vol_2 != 0:
            average_2 = weighted_sum_2 / total_vol_2
        else:
            average_2 = 0

        if total_vol_3 != 0:
            average_3 = weighted_sum_3 / total_vol_3
        else:
            average_3 = 0

        if total_vol_4 != 0:
            average_4 = weighted_sum_4 / total_vol_4
        else:
            average_4 = 0

        if total_vol_5 != 0:
            average_5 = weighted_sum_5 / total_vol_5
        else:
            average_5 = 0

        if total_vol_6 != 0:
            average_6 = weighted_sum_6 / total_vol_6
        else:
            average_6 = 0


        ask_ref= ask_exchange.replace('_pairs','')
        bid_ref=bid_exchange.replace('_pairs','')


        weighted_orderbook = pd.DataFrame({
            f'{pair_name} {ask_ref} Ask': [ask_1, ask_2, ask_3, ask_4, ask_5,ask_6, ],
            f'{pair_name} {bid_ref} Bid': [bid_1, bid_2, bid_3, bid_4, bid_5,bid_6, ],
            'Vol': [vol_1, vol_2, vol_3, vol_4, vol_5,vol_6, ],
            'Min Prof': ['1%', '0.75%', '0.5%', '0.25%', '0.1%', '0.01 %',],
            'Weighted': [average_1, average_2, average_3, average_4, average_5, average_6,]
        })


        depth_rate_list.append(weighted_orderbook)

        counter += 1

    return depth_rate_list







