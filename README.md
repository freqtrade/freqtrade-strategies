# Freqtrade strategies

This Git repo contains free buy/sell strategies for [Freqtrade](https://github.com/freqtrade/freqtrade).

All strategies should work with a freqtrade version of 2022.4 or newer.

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
- [Contribute](#share-your-own-strategies-and-contribute-to-this-repo)
- [FAQ](#faq)
  - [What is Freqtrade?](#what-is-freqtrade)
  - [What includes these strategies?](#what-includes-these-strategies)
  - [How to install a strategy?](#how-to-install-a-strategy)
  - [How to test a strategy?](#how-to-test-a-strategy)
  - [How to create/optimize a strategy?](https://www.freqtrade.io/en/latest/strategy-customization/)

## Free trading strategies

Strategies from this repo are free to use, though they are provided as-is and without any warranty.
They also mostly should serve as a starting point for your own strategies, not as "ready to use" strategies.
Feel free to use and/or update them to your likings.

Some may only work in specific market conditions, while others are more "general purpose" strategies.
It's noteworthy that further optimization to the exchange and Pairs used will usually result in better outcomes.

Please keep in mind, results will heavily depend on the pairs, timeframe and timerange used to backtest - so please run your own backtests that mirror your usecase, to evaluate each strategy for yourself.

The results above should serve as a general outline to demonstrate the number of trades to expect. Actual performance will be different based on various factors.

## Share your own strategies and contribute to this repo

Feel free to send your strategies, comments, optimizations and pull requests via an 
[Issue ticket](https://github.com/freqtrade/freqtrade-strategies/issues/new) or as a [Pull request](https://github.com/freqtrade/freqtrade-strategies/pulls) enhancing this repository.

## FAQ

### What is Freqtrade?

[Freqtrade](https://github.com/freqtrade/freqtrade) Freqtrade is a free and open source crypto trading bot written in Python.
It is designed to support all major exchanges and be controlled via Telegram. It contains backtesting, plotting and money management tools as well as strategy optimization by machine learning.

### What includes these strategies?

Each Strategies includes:  

- [x] **Minimal ROI**: Minimal ROI optimized for the strategy.
- [x] **Stoploss**: Optimal stoploss.
- [x] **Buy signals**: Result from Hyperopt or based on existing trading strategies.
- [x] **Sell signals**: Result from Hyperopt or based on existing trading strategies.
- [x] **Indicators**: Includes the indicators required to run the strategy.

Best backtest multiple strategies with the exchange and pairs you're interested in, and fine tune the strategy to the markets you're trading.

### How to install a strategy?

First you need a [working Freqtrade](https://freqtrade.io).

Once you have the bot on the right version, follow this steps:

1. Select the strategy you want. All strategies of the repo are into 
[user_data/strategies](https://github.com/freqtrade/freqtrade-strategies/tree/main/user_data/strategies)
2. Copy the strategy file
3. Paste it into your `user_data/strategies` folder
4. Run the bot with the parameter `--strategy <STRATEGY CLASS NAME>` (ex: `freqtrade trade --strategy Strategy001`)

More information [about backtesting](https://www.freqtrade.io/en/latest/backtesting/) and [strategy customization](https://www.freqtrade.io/en/latest/strategy-customization/).

### How to test a strategy?

Let assume you have selected the strategy `strategy001.py`:

#### Simple backtesting

```bash
freqtrade backtesting --strategy Strategy001
```

#### Refresh your test data

```bash
freqtrade download-data --days 100
```

*Note:* Generally, it's recommended to use static backtest data (from a defined period of time) for comparable results.

Please check out the [official backtesting documentation](https://www.freqtrade.io/en/latest/backtesting/) for more information.
