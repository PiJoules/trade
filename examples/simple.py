#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Print out closing prices as they are processed.
"""

from trade.strategy import BaseStrategy
from trade.datafeed import YahooFeed
from trade.broker import BacktestBroker


class SimpleStrategy(BaseStrategy):
    def __init__(self, feed, symbol, cash):
        super().__init__(feed, BacktestBroker(cash, feed))
        self.__symbol = symbol

    def on_data(self, data):
        data = data[self.__symbol]
        self.info(data.close)


# Load the yahoo feed from the CSV file
feed = YahooFeed()
feed.add_data_from_csv("orcl", "orcl_2000.csv")

# Evaluate the strategy with the feed's data
strategy = SimpleStrategy(feed, "orcl", 1000000)
strategy.run()

