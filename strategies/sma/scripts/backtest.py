#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Run backtests for this strategy.
"""

import sys

from trade import Feed
from ..strategy import SMAStrategy


def get_args():
    from argparse import ArgumentParser
    parser = ArgumentParser("SMA strategy parser")

    parser.add_argument("-i", "--input", action="append", default=[],
                        required=True, help="Feed inputs.")
    parser.add_argument("-w", "--window", type=int, default=20,
                        help="Window size for sma (default: %(default)d.")
    parser.add_argument("-c", "--cash", type=int, default=1000,
                        help="Starting cash (default: %(default)d).")

    return parser.parse_args()


def main():
    args = get_args()

    # Create feed
    feed = Feed(*args.input, buffer_size=args.window)

    # Evaluate strategy with the feed's data
    strategy = SMAStrategy(feed, args.window, args.cash)
    strategy.run()
    print("Final portfolio value: ${:.2f}".format(strategy.total_value))

    return 0


if __name__ == "__main__":
    sys.exit(main())

