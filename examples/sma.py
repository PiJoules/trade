#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Print out simple moving average of closing prices as they are processed.
"""

from trade.strategy import BaseStrategy
from trade.barfeed import YahooFeed


class SMAStrategy(BaseStrategy):

    def __init__(self, window_size):
        super(SMAStrategy, self).__init__()
        self.__window = []
        self.__window_size = window_size

    def on_bar(self, bar):
        window = self.__window
        window.append(bar.close)
        window_size = self.__window_size
        sma = None
        if len(window) > window_size:
            del window[0]
        if len(window) == window_size:
            sma = (1.0 * sum(window)) / window_size

        print(bar.datetime, bar.close, sma)


def main():
    # Load the yahoo feed from the CSV file
    feed = YahooFeed()
    feed.add_bars_from_csv("orcl", "orcl_2000.csv")

    # Evaluate the strategy with the feed's data
    strategy = SMAStrategy(15)
    strategy.run(feed)


if __name__ == "__main__":
    main()

