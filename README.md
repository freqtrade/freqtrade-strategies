# Freqtrade strategies

This Git repo contains free buy/sell strategies for [Freqtrade](https://github.com/freqtrade/freqtrade) >= `0.16.0`.

## Disclaimer

These strategies are for educational purposes only. Do not risk money 
which you are afraid to lose. USE THE SOFTWARE AT YOUR OWN RISK. THE 
AUTHORS AND ALL AFFILIATES ASSUME NO RESPONSIBILITY FOR YOUR TRADING 
RESULTS. 

Always start by testing strategies with a backtesting then run the 
trading bot in Dry-run. Do not engage money before you understand how 
it works and what profit/loss you should expect.

We strongly recommend you to have coding and Python knowledge. Do not 
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
    - [Can I have your configuration file?](#can-i-have-your-configuration-file)
    - [How to create/optimize a strategy?](https://github.com/freqtrade/freqtrade/blob/develop/docs/bot-optimization.md)

## Free trading strategies
Value below are result from backtesting from 2018-01-10 to 2018-01-30 and  
`experimental.sell_profit_only` enabled. More detail on each strategy 
page.

|  Strategy | Buy count | AVG profit % | Total profit | AVG duration | Backtest period |
|-----------|-----------|--------------|--------------|--------------|-----------------|
| [Strategy 001](https://github.com/freqtrade/freqtrade-strategies/issues/1) | 55 | 0.05 | 0.00012102 |  476.1 | 2018-01-10 to 2018-01-30 |
| [Strategy 002](https://github.com/freqtrade/freqtrade-strategies/issues/2) | 9 | 3.21 | 0.00114807 |  189.4 | 2018-01-10 to 2018-01-30 |
| [Strategy 003](https://github.com/freqtrade/freqtrade-strategies/issues/3) | 14 | 1.47 | 0.00081740 |  227.5 | 2018-01-10 to 2018-01-30 | 
| [Strategy 004](https://github.com/freqtrade/freqtrade-strategies/issues/4) | 37 | 0.69 | 0.00102128 |  367.3 | 2018-01-10 to 2018-01-30 | 
| [Strategy 005](https://github.com/freqtrade/freqtrade-strategies/issues/11) | 180 | 1.16 | 0.00827589 |  156.2 | 2018-01-10 to 2018-01-30 |


Strategies from this repo are free to use. Feel free to update them. 
Most of them  were designed from Hyperopt calculations.

## Share your own strategies and contribute to this repo
Feel free to send your strategies, comments, optimizations and pull requests via an 
[Issue ticket](https://github.com/freqtrade/freqtrade-strategies/issues/new).  

## FAQ

### What is Freqtrade?
[Freqtrade](https://github.com/freqtrade) is a Simple High 
frequency trading bot for crypto currencies designed to support 
 
exchanges and be controlled via Telegram built by [gcarq@](https://github.com/gcarq) and the
[core-dev team](https://github.com/orgs/freqtrade/teams/core-dev).

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

All strategies tests are explain on their own tickets.  
For each strategies, we generally run backtests twice with `experimental.sell_profit_only`
enabled and disabled.

### How to install a strategy?

First you need a [working Freqtrade](https://github.com/freqtrade/freqtrade/blob/develop/docs/index.md) 
in version >= 0.16.0. 

Once you have the bot on the right version, follow this steps:

1. Select the strategy you want. All strategies of the repo are into 
[user_data/strategies](https://github.com/freqtrade/freqtrade/tree/develop/user_data/strategies)
2. Copy the strategy file
3. Paste it into your `user_data/strategies` folder
4. Run the bot with the parameter `-s <STRATEGY CLASS NAME>` (ex: `python3 ./freqtrade/main.py -s Strategy001`)

### How to test a strategy?

Let assume you have selected the strategy `strategy001.py`:

#### Simple backtesting

```bash
python3 ./freqtra
e/main.py -s Strategy001 backtesting
```

#### Refresh your test data

```bash
python3 ./freqtrade/main.py -s Strategy001 backtesting --refresh-pairs-cached
```

#### Test with live data

```bash
python3 ./freqtrade/main.py -s Strategy001 backtesting --live
```

## Can I have your configuration file?

You will find them into [user_data/](https://github.com/freqtrade/freqtrade-strategies/tree/master/user_data) folder.
