#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
- If the adjusted close price is above the SMA(15) we enter a long position
  (we place a buy market order).
- If a long position is in place, and the adjusted close price drops below
  the SMA(15) we exit the long position (we place a sell market order).
"""

from trade import (Feed, Portfolio, Broker, Order, TransactionType,
                   BaseStrategy)


class SMAStrategy(BaseStrategy):

    def __init__(self, window_size, cash):
        self.__broker = Broker()
        self.__portfolio = Portfolio(cash=cash)
        super().__init__(self.__broker, self.__portfolio)
        self.__window = []
        self.__window_size = window_size

    @property
    def cash(self):
        return self.__portfolio.total_value

    def buy(self, bar, sma, amount):
        order = Order(symbol=bar.symbol,
                      volume=amount,
                      price=bar.close,
                      transaction=TransactionType.BUY,
                      timestamp=bar.timestamp)
        self.__broker.place(order)
        print("{}: BUY at ${:.2f} (balance ${:.2f})"
              .format(bar.datetime, bar.close, self.__portfolio.cash))

    def sell(self, bar, sma, amount):
        order = Order(symbol=bar.symbol,
                      volume=amount,
                      price=bar.close,
                      transaction=TransactionType.SELL,
                      timestamp=bar.timestamp)
        self.__broker.place(order)
        print("{}: SELL at ${:.2f} (balance ${:.2f})"
              .format(bar.datetime, bar.close, self.__portfolio.cash))

    def on_bar(self, bar):
        window = self.__window
        window.append(bar.close)
        window_size = self.__window_size
        sma = None
        if len(window) > window_size:
            del window[0]
        if len(window) == window_size:
            sma = sum(window) / window_size

        if sma is None:
            return

        if (not self.__portfolio.contains_symbol(bar.symbol) and
                bar.close > sma):
            self.buy(bar, sma, 10)
        elif (self.__portfolio.contains_symbol(bar.symbol) and
                bar.close < sma):
            self.sell(bar, sma, 10)


def main():
    # Load the yahoo feed from the CSV file
    feed = Feed()
    feed.add_file("orcl_2000.jsonl.gz")

    # Evaluate the strategy with the feed's data
    strategy = SMAStrategy(20, 1000)
    strategy.run(feed)
    print("Final portfolio value: ${:.2f}".format(strategy.cash))


if __name__ == "__main__":
    main()

