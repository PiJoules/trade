#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Plot data from this strategy.
"""

import sys

from trade import Feed
from ..strategy import SMAStrategy


def get_args():
    from argparse import ArgumentParser
    parser = ArgumentParser("Plot data handled by strategy.")

    parser.add_argument("input", default=[], nargs="+", help="Feed inputs.")
    parser.add_argument("-o", "--output", help="Output file to save plot.")
    parser.add_argument("-w", "--window_size", type=int, default=22,
                        help="SMA window size.")
    parser.add_argument("-c", "--cash", type=int, help="")

    return parser.parse_args()


def main():
    args = get_args()

    symbol = None
    feed = Feed(*args.input)
    strategy = SMAStrategy(feed, args.window_size, args.cash, silent=True)
    strategy.run()

    # Ready outputs
    outputs = []

    return 0


if __name__ == "__main__":
    sys.exit(main())

