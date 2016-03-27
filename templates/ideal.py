#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Find the ideal parameters for this strategy.
"""

import sys

from trade import max_vals
from ..strategy import Strategy


def get_args():
    from argparse import ArgumentParser
    parser = ArgumentParser("Strategy parser")

    parser.add_argument("-i", "--input", action="append", default=[],
                        required=True, help="Feed inputs.")
    parser.add_argument("-v", "--verbose", action="store_true", default=False,
                        help="Logging verbosity.")

    return parser.parse_args()


def main():
    args = get_args()

    print("Testing parameters:")
    print("inputs:", args.input)
    print("...")

    max_val, max_val_args = max_vals(
        Strategy, args.input, silent=not args.verbose)

    print("Max return: ${}".format(max_val))
    print("Args associacted with max:", max_val_args)

    return 0


if __name__ == "__main__":
    sys.exit(main())

