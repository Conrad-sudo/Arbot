# Cryptocurrency Arbitrage Trading Bot

This project is a cryptocurrency arbitrage trading bot that monitors price discrepancies across various exchanges. It identifies potential arbitrage opportunities by comparing prices for the same trading pairs on different platforms.

## Features

- Fetches live market data from multiple exchanges.
- Identifies common trading pairs across different platforms.
- Calculates potential arbitrage profits.
- Generates reports on available trading pairs and their respective prices.
- Error handling and logging for better debugging.

## Requirements
- Python 3.x
- Requests library
  

## Supported Exchanges

The bot currently supports the following exchanges:
- Coinbase
- Kraken
- OKX
- Huobi
- OKCoin
- KuCoin
- Bittrex
- Bitget
- Binance

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/crypto-arbitrage-bot.git
2. cd crypto-arbitrage-bot
3. Set up virtual environment: **python3 -m venv venv**
4. Activate venv **source venv/bin/activate**
5. Instal dependencies: **pip install requests**
6. Initialize trade pairs by running init_trade_pairs in main.py


The bot initializes by fetching the latest market data from the supported exchanges and creating a list of tradable pairs. It will save the results in JSON files for further analysis.

# Finding Arbitrage Opportunities
The bot can find arbitrage opportunities between two exchanges for a given trading pair. The function find_arb(pair, ask_exchange, bid_exchange) computes potential profits and provides a report.

# Configuration
You may want to configure the following settings:

- Exchange URLs: Modify the URLs in the script if necessary.
- Red List: Update the red_list to exclude specific pairs from trading.

# Functions Overview
- get_ticker(url): Fetches JSON data from the given API URL.
- get_kraken(kraken_market): Extracts tradable pairs from Kraken.
- get_coinbase(coinbase_market): Extracts tradable pairs from Coinbase.
- get_okx(okx_market): Extracts tradable pairs from OKX.
- get_huobi(huobi_market): Extracts tradable pairs from Huobi.
- get_okcoin(okcoin_market): Extracts tradable pairs from OKCoin.
- get_kucoin(kucoin_market): Extracts tradable pairs from KuCoin.
- get_bittrex(bittrex_market): Extracts tradable pairs from Bittrex.
- get_bitget(bitget_market): Extracts tradable pairs from Bitget.
- find_common_pairs(pair_1, pair_2): Identifies common pairs between two exchanges.
- get_trade_pairs(ask_exchange, bid_exchange): Retrieves trade pairs for given exchanges.
- select_pairs(trade_pairs, pair, ask_exchange, bid_exchange, ask_sign, bid_sign): Selects pairs based on criteria.
- sort_price(selected_trade_pairs, bid_exchange, ask_exchange): Retrieves bid and ask prices for selected pairs.
- calc_surf_rate(price_dict, selected_trade_pairs, ask_exchange, bid_exchange): Calculates potential profit opportunities.
- get_orderbook(surface_rate_list, ask_exchange, bid_exchange, depth): Retrieves the orderbook for specified pairs.

- find_arb(pair, ask_exchange, bid_exchange):
    """
    Calculate arbitrage opportunities between two exchanges for a given trading pair.

    Args:
        pair (str): The trading pair to check for arbitrage (e.g., "BTC/USD").
        ask_exchange (str): The exchange from which to buy (e.g., "binance").
        bid_exchange (str): The exchange from which to sell (e.g., "kraken").

    Returns:
        list: A list of rates indicating potential profit opportunities, or an error message.
    """
    ...



