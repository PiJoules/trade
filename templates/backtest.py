#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Run backtests for this strategy.
"""

import sys

from trade import Feed
from ..strategy import Strategy


def get_args():
    from argparse import ArgumentParser
    parser = ArgumentParser("SMA strategy parser")

    parser.add_argument("input", default=[], nargs="+", help="Feed inputs.")

    return parser.parse_args()


def main():
    args = get_args()

    # Create feed.
    feed = Feed(*args.input)

    # Evaluate strategy with the feed's data
    strategy = Strategy(feed)
    strategy.run()

    return 0


if __name__ == "__main__":
    sys.exit(main())

