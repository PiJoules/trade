#!/usr/bin/env python

"""
Module for handling yahoo interface.
"""

from datetime import date
from .csv import download_csv

YAHOO_BASE = "http://ichart.finance.yahoo.com/table.csv"


def download_yahoo_csv(symbol, start, end, freq):
    """Download stock data from yahoo finance."""
    # Months are zero-indexed
    return download_csv(YAHOO_BASE, params={
        "s": symbol,
        "a": start.month - 1,
        "b": start.day,
        "c": start.year,
        "d": end.month - 1,
        "e": end.day,
        "f": end.year,
        "g": freq,
        "ignore": ".csv"
    })


def download_daily_data(symbol, year, output_file):
    """Download daily stock data for a given stock symbol over 1 year."""
    csv_text = download_yahoo_csv(symbol, date(year, 1, 1),
                                  date(year, 12, 31), "d")
    with open(output_file, "w") as output:
        output.write(csv_text)


def get_args():
    """Parse cmd line args."""
    from argparse import ArgumentParser
    parser = ArgumentParser("Download Yahoo data")

    parser.add_argument("symbol", help="Stock symbol.")
    parser.add_argument("year", type=int,
                        help="Year in format YYYY.")
    parser.add_argument("output", help="Output file to save csv.")

    return parser.parse_args()


def download_daily():
    """Cmd line function for calling download_yahoo_csv."""
    args = get_args()
    download_daily_data(args.symbol, args.year, args.output)

