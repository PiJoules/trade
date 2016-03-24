#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Find the ideal parameters for this strategy.
"""

import sys

from trade import Feed, test_vals
from ..strategy import SMAStrategy


def get_args():
    from argparse import ArgumentParser
    parser = ArgumentParser("SMA strategy parser")

    parser.add_argument("-i", "--input", action="append", default=[],
                        required=True, help="Feed inputs.")
    parser.add_argument("--min-window", type=int, required=True,
                        help="Min window size to test.")
    parser.add_argument("--max-window", type=int, required=True,
                        help="Max window size to test.")
    parser.add_argument("-c", "--cash", type=int, default=1000,
                        help="Starting cash (default: %(default)d).")

    return parser.parse_args()


def main():
    args = get_args()

    assert args.max_window > args.min_window

    print("Testing parameters:")
    print("inputs:", args.input)
    print("window size: [{}, {}]".format(args.min_window, args.max_window))
    print("starting cash: ${}".format(args.cash))
    print("...")

    feed = Feed()
    feed.add_files(args.input)

    max_val, max_val_args = test_vals(
        SMAStrategy, feed, range(args.min_window, args.max_window + 1),
        [args.cash])

    print("Max return: ${}".format(max_val))
    print("Args associacted with max:", max_val_args)

    return 0


if __name__ == "__main__":
    sys.exit(main())

