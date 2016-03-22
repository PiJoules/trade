#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Print out closing prices as they are processed.
"""

from trade import BaseStrategy
from trade import Feed


class SimpleStrategy(BaseStrategy):

    def on_bar(self, bar):
        print(bar.datetime, "{:.2f}".format(bar.close))


def get_args():
    from argparse import ArgumentParser
    parser = ArgumentParser("Simple Strategy")
    parser.add_argument("input", help="Input compressed jsonl file.")
    return parser.parse_args()


def main():
    args = get_args()

    # Load the yahoo feed from the CSV file
    feed = Feed()
    feed.add_file(args.input)

    # Evaluate the strategy with the feed's data
    strategy = SimpleStrategy()
    strategy.run(feed)


if __name__ == "__main__":
    main()

