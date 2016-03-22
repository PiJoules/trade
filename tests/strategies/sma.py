#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Print out simple moving average of closing prices as they are processed.
"""

from trade import Feed, BaseStrategy


class SMAStrategy(BaseStrategy):

    def __init__(self, window_size):
        super().__init__()
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

        if sma:
            print("{} {:.2f} {:.2f}".format(bar.datetime, bar.close, sma))


def get_args():
    from argparse import ArgumentParser
    parser = ArgumentParser("SMA Strategy")
    parser.add_argument("input", help="Input compressed jsonl file.")
    return parser.parse_args()


def main():
    args = get_args()

    # Load the yahoo feed from the CSV file
    feed = Feed()
    feed.add_file(args.input)

    # Evaluate the strategy with the feed's data
    strategy = SMAStrategy(15)
    strategy.run(feed)


if __name__ == "__main__":
    main()

