#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Print out closing prices as they are processed.
"""

from trade.strategy import BaseStrategy
from trade import Feed


class SimpleStrategy(BaseStrategy):

    def on_bar(self, bar):
        print(bar.datetime, bar.timestamp, bar.close)


def main():
    # Load the yahoo feed from the CSV file
    feed = Feed()
    feed.add_file("orcl_2000.jsonl.gz")

    # Evaluate the strategy with the feed's data
    strategy = SimpleStrategy()
    strategy.run(feed)


if __name__ == "__main__":
    main()

