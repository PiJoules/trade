#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Print out closing prices as they are processed.
"""

from trade.strategy import BaseStrategy
from trade.barfeed import YahooFeed


class SimpleStrategy(BaseStrategy):

    def on_bar(self, bar):
        print(bar.datetime, bar.close)


def main():
    # Load the yahoo feed from the CSV file
    feed = YahooFeed()
    feed.add_bars_from_csv("orcl", "orcl_2000.csv")

    # Evaluate the strategy with the feed's data
    strategy = SimpleStrategy()
    strategy.run(feed)


if __name__ == "__main__":
    main()

