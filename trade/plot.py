#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for plotting data from a compressed jsonl file with ONLY 1 symbol.
"""

import matplotlib.pyplot as plot
import matplotlib.dates as dates

from .jsonl import JSONLReader
from .feed import Feed
from datetime import datetime


def get_args():
    from argparse import ArgumentParser
    parser = ArgumentParser("Plot market data")

    parser.add_argument("input", default=[], nargs="+", help="Feed inputs.")
    parser.add_argument("-o", "--output", help="Output file to save plot.")
    parser.add_argument("--daily", action="store_true", default=False,
                        help="Input is daily data instead of intra day.")

    series_group = parser.add_argument_group(
        title="Series", description="Series to plot. Closing is always "
        "included.")
    series_group.add_argument("--open", action="store_true", default=False)
    series_group.add_argument("--high", action="store_true", default=False)
    series_group.add_argument("--low", action="store_true", default=False)

    return parser.parse_args()


def main():
    args = get_args()

    # Ready data
    symbol = None
    times = []
    close = []
    open_ = []
    high = []
    low = []

    feed = Feed(*args.input)
    for bar in feed:
        jsonl = bar.dict()
        # Check only 1 symbol is published
        if symbol is not None:
            assert symbol == jsonl["symbol"]
        else:
            symbol = jsonl["symbol"]

        # Add data
        close.append(jsonl["close"])
        times.append(datetime.fromtimestamp(jsonl["timestamp"]))
        if args.open:
            open_.append(jsonl["open"])
        if args.high:
            high.append(jsonl["high"])
        if args.low:
            low.append(jsonl["low"])

    # Ready outputs
    outputs = [times, close, "b"]
    legend = ["Close"]
    if args.open:
        outputs += [times, open_, "r"]
        legend.append("Open")
    if args.high:
        outputs += [times, high, "g"]
        legend.append("High")
    if args.low:
        outputs += [times, low, "c"]
        legend.append("Low")

    # Formatting
    date_ = times[0].date()
    start_time = times[0].time()
    end_time = times[-1].time()
    end_date = times[-1].date()

    # Format plot
    plot.figure(figsize=(20, 10))
    if not args.daily:
        plot.gca().xaxis.set_major_formatter(dates.DateFormatter("%H:%M:%S"))
        plot.gca().xaxis.set_major_locator(dates.HourLocator())
        plot.gca().xaxis.set_minor_locator(dates.MinuteLocator())
        title = "Market data for {} on {}".format(symbol, date_)
        xlabel = "Time ({} - {})".format(start_time, end_time)
    else:
        title = "Market data for {} from {} to {}".format(
            symbol, date_, end_date)
        xlabel = "Time"

    plot.plot(*outputs)
    plot.grid()
    plot.xlabel(xlabel)
    plot.ylabel("Price (USD)")
    plot.title(title)
    plot.legend(legend)

    # Save/show output
    if args.output:
        plot.savefig(args.output)
    plot.show()

