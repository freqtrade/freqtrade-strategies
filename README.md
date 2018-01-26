# Freqtrade strategies

This Git repo contains free buy/sell strategies for [Freqtrade](https://github.com/gcarq/freqtrade) >= `0.16.0`.


## Disclaimer
These strategies are for educational purposes only. Do not risk money 
which you are afraid to lose. USE THE SOFTWARE AT YOUR OWN RISK. THE 
AUTHORS AND ALL AFFILIATES ASSUME NO RESPONSIBILITY FOR YOUR TRADING 
RESULTS. 

Always start by testing strategies with a backtesting then run the 
trading bot in Dry-run. Do not engage money before you understand how 
it works and what profit/loss you should expect.

I strongly recommend you to have coding and Python knowledge. Do not 
hesitate to read the source code and understand the mechanism of this 
bot.

## Table of Content
- [Free trading strategies](#free-trading-strategies)
- [Contributes](#Contributes)
- [FAQ](#faq)
    - [What is Freqtrade?](#what-is-freqtrade)
    - [What includes these strategies?](#what-includes-these-strategies)
    - [How were tested the strategies?](#how-were-tested-the-strategies)
    - [How to install a strategy?](#how-to-install-a-strategy)
    - [How to test a strategy?](#how-to-test-a-strategy)
    - [Which coins were tested?](#which-coins-were-tested)
    - [Can I have your configuration file?](#can-i-have-your-configuration-file)
    - [Can I have your dataset?](#can-i-have-your-dataset)
    - [How did you build dataset?](#how-did-you-build-dataset)
    - [How to create/optimize a strategy?](https://github.com/gcarq/freqtrade/blob/develop/docs/bot-optimization.md)
- [Offer me a coffee](#offer-me-a-coffee)

## Free trading strategies
Value below are result from backtesting from 2017-12-19 to 2017-01-20 and  
`experimental.sell_profit_only` enabled. More detail on each strategy 
page.

|  Strategy | Buy count | AVG profit % | Total profit | AVG duration |
|-----------|-----------|--------------|--------------|--------------|
| [Strategy 001](https://github.com/glonlas/freqtrade-strategies/issues/1) | 287 | 2.39 | 0.02763202 |  1306.3 |
| [Strategy 002](https://github.com/glonlas/freqtrade-strategies/issues/2) | 158 | 2.67 | 0.01686667 |  387.9 |
| [Strategy 003](https://github.com/glonlas/freqtrade-strategies/issues/3) | 147 | 2.21 | 0.01277113 |  694.9 | 
| [Strategy 004](https://github.com/glonlas/freqtrade-strategies/issues/4) | 232 | 2.11 | 0.01977185 |  455.3 | 


Strategies from this repo are free to use and feel free to update them. 
Most of them  were designed from Hyperopt calculations.

## Contributes
Feel free to send your comments, optimizations and requests via an 
[Issue ticket](https://github.com/glonlas/freqtrade-strategies/issues/new).  

### Strategy requests
Are you looking to implement a new strategy, or one found on atrading 
Forum/Chan?  
You can request it via 
[Issue ticket](https://github.com/glonlas/freqtrade-strategies/issues/new). 
Please follow the template questions. Request that does not follow the 
template will be removed. I cannot promise to implement all of them, 
but will do my best to help.

## FAQ

### What is Freqtrade?
[Freqtrade](https://github.com/gcarq/freqtrade) is a Simple High 
frequency trading bot for crypto currencies designed to support multi 
exchanges and be controlled via Telegram built by [gcarq@](https://github.com/gcarq).

This bot is similar other trading bot like 
[Gekko](https://github.com/askmike/gekko), and 
[Zenbot](https://github.com/DeviaVir/zenbot)

### What includes these strategies?
Each Strategies includes:  
- [x] **Minimal ROI**: Minimal ROI optimized for the strategy.
- [x] **Stoploss**: Optimimal stoploss calculated based on hyperopt result.
- [x] **Buy Strategy**: Result from Hyperopt or based on exisiting trading strategies.
- [x] **Sell Strategy**
- [x] **Indicators**: Includes the indicators required to run the strategy.
- [x] **Hyperopt configuration:** To tune the strategy parameters.
- [x] **Backtesting results** 

### How were tested the strategies?
All strategies are tested with the dataset from this repo. The data set 
is located into [user_data/data](https://github.com/glonlas/freqtrade-strategies/tree/master/user_data/data) folder.  
For each strategies, I run backtests for 2 Period and 2 parameters:
 `experimental.sell_profit_only` enabled and  
`experimental.sell_profit_only` disabled

#### Period 1: From 2017-11-19 to 2017-12-20  
1. `experimental.sell_profit_only` at `true` (Config file [user_data/config-profit-on.json](https://github.com/glonlas/freqtrade-strategies/blob/master/user_data/config-profit-on.json)).
2. `experimental.sell_profit_only` at `false` (Config file [user_data/config-profit-off.json](https://github.com/glonlas/freqtrade-strategies/blob/master/user_data/config-profit-off.json)). 

#### Period 2: From 2017-12-19 to 2017-01-20
1. `experimental.sell_profit_only` at `true` (Config file [user_data/config-profit-on.json](https://github.com/glonlas/freqtrade-strategies/blob/master/user_data/config-profit-on.json)).
2. `experimental.sell_profit_only` at `false` (Config file [user_data/config-profit-off.json](https://github.com/glonlas/freqtrade-strategies/blob/master/user_data/config-profit-off.json)). 

### How to install a strategy?
First you need a [working Freqtrade](https://github.com/gcarq/freqtrade/blob/feature/custom_strategy/docs/index.md) 
in version >= 0.16.0. 

**Note:** This version is not merged yet but you can find into the branch `feature/custom_strategy`.
```bash
git clone https://github.com/gcarq/freqtrade.git
git checkout feature/custom_strategy
```

Once you have the bot on the right version, follow this steps:
1. Select the strategy you want. All strategies of the repo are into 
(user_data/strategies](https://github.com/glonlas/freqtrade-strategies/tree/feature/custom_strategy/user_data/strategies)
2. Copy the strategy file
3. Paste it into your `user_data/strategies` folder
4. Run the bot with the parameter `-s <STRATEGY_FILE_NAME_WITHOUT_.py>` (ex: `python3 ./freqtrade/main.py -s strategy001`)

### How to test a strategy?
Let assume you have selected the strategy `strategy-001.py`:

**Simple backtesting**
```bash
python3 ./freqtrade/main.py -s strategy-001 backtesting --realistic-simulation
```

**Refresh your test data**
```bash
python3 ./freqtrade/main.py -s strategy-001 backtesting --realistic-simulation -r
```

**Test with live data**
```bash
python3 ./freqtrade/main.py -s strategy-001 backtesting --realistic-simulation -l
```

### Which coins were tested?
You will find the list of coin tested into the configuration files 
(`user_data/config-profit-on.json` and 
`user_data/config-profit-off.json`)

|  Pair | Tested |
|-------|--------|
| BTC_ADA | Yes
| BTC_NEO | Yes | 
| BTC_NXT | Yes | 
| BTC_MCO | Yes | 
| BTC_ETH | Yes | 
| BTC_BCC | Yes | 
| BTC_VOX | Yes | 
| BTC_GUP | Yes | 
| BTC_SC | Yes | 
| BTC_VTC | Yes | 
| BTC_STRAT | Yes | 
| BTC_OMG | Yes | 
| BTC_OK | Yes | 
| BTC_EDG | Yes | 
| BTC_STORJ | Yes | 
| BTC_EMC2 | Yes | 
| BTC_XLM | Yes | 
| BTC_LSK | Yes | 
| BTC_SYS | Yes | 
| BTC_POWR | Yes | 
| BTC_PAY | Yes | 
| BTC_DGB | Yes | 
| BTC_ETC | Yes | 
| BTC_XRP | Yes | 
| BTC_LTC | Yes | 
| BTC_IOP | Yes | 
| BTC_RCN | Yes | 
| BTC_BTG | Yes | 
| BTC_MONA | Yes | 
| BTC_SALT | Yes | 
| BTC_DASH | Yes | 
| BTC_QTUM | Yes | 
| BTC_CVC | Yes | 
| BTC_KMD | Yes | 
| BTC_XEM | Yes | 
| BTC_XMR | Yes | 
| BTC_ZEC | Yes | 
| BTC_WAVES | Yes | 
| BTC_PIVX | Yes | 
| BTC_XZC | Yes | 
| BTC_DOGE | No, this pair is blacklisted |

## Can I have your configuration file?
You will find them into [user_data/](https://github.com/glonlas/freqtrade-strategies/tree/master/user_data) folder.

## Can I have your datasets?
Yes of course! Datasets are into 
[user_data/data](https://github.com/glonlas/freqtrade-strategies/tree/master/user_data/data) 
folder. Download and use them.

## How did you build dataset?
I am using data collected from Bittrex and run the script 
`scripts/extract_data.py`
```bash
python3 scripts/extract_data.py -f user_data/data/complete_data -d user_data/data/2017-11-19_2017-12-19 -s 2017-11-19 -e 2017-12-20
python3 scripts/extract_data.py -f user_data/data/complete_data -d user_data/data/2017-12-19_2018-01-19 -s 2017-12-19 -e 2018-01-20
```

# Offer me a coffee
This repo is made for you to improve your trading strategies. If you are
happy with the result of your strategy, feel free to offer me a coffee :)

- BTC: 1KouEQdEKGiFGvm9iCb5K9pkUqnsASqmGS
- ETH: 0x767D8AfB3B31131cBbf5b7318D2046996c9a40f2
- LTC: LXFPwMs38DMj6ecD4xWEPnWjNAjp78uNZM
