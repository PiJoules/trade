#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for handling bar data download from yahoo finance.
"""

import csv

from datetime import datetime


class Bar(object):
    """Class represnting a row of data."""

    __slots__ = ("datetime", "open", "high", "low", "close", "volume",
                 "adjusted_close", "symbol")

    def __init__(self, **kwargs):
        open_ = kwargs["open"]
        high = kwargs["high"]
        low = kwargs["low"]
        close = kwargs["close"]
        recv_time = kwargs["datetime"]

        # Check params
        if high < low:
            raise Exception("high < low at '{}'".format(recv_time))
        if high < open_:
            raise Exception("high < open at '{}'".format(recv_time))
        if high < close:
            raise Exception("high < close at '{}'".format(recv_time))
        if low > open_:
            raise Exception("low > open at '{}'".format(recv_time))
        if low > close:
            raise Exception("low > close at '{}'".format(recv_time))

        self.datetime = recv_time
        self.open = open_
        self.high = high
        self.low = low
        self.close = close
        self.volume = kwargs["volume"]
        self.adjusted_close = kwargs["adj_close"]
        self.symbol = kwargs["symbol"]


class YahooFeed(object):
    """
    Yahoo bar feed data parser.

    Format:
    Date,Open,High,Low,Close,Volume,Adj Close
    2000-12-29,30.875,31.3125,28.6875,29.0625,31702200,26.989868
    2000-12-28,30.5625,31.625,30.375,31.0625,25053600,28.847236
    2000-12-27,30.375,31.0625,29.375,30.6875,26437500,28.498979
    ...
    """

    DATE_FORMAT = "%Y-%m-%d"

    def __init__(self, symbol_map=None):
        symbol_map = symbol_map or {}
        self.__bars = []

        self.add_bars_from_csvs(symbol_map)

    def add_bars_from_csvs(self, symbol_map):
        """
        Add bar data from multiple csvs to this feed.

        symbol_map:
            Dict mapping symbol => csvpath
        """
        # Parse csv
        bars = []
        date_format = self.DATE_FORMAT
        for symbol, csvpath in symbol_map.items():
            with open(csvpath, "r") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    recv_time = datetime.strptime(row["Date"], date_format)
                    bar = Bar(datetime=recv_time,
                              open=float(row["Open"]),
                              high=float(row["High"]),
                              low=float(row["Low"]),
                              close=float(row["Close"]),
                              volume=int(row["Volume"]),
                              adj_close=float(row["Adj Close"]),
                              symbol=symbol)
                    bars.append(bar)

        # Add the new bars and sort by receive time
        self.__bars = sorted(bars + self.__bars, key=lambda x: x.datetime)

    def add_bars_from_csv(self, symbol, csvpath):
        """Add bar data from a single csv to this feed."""
        self.add_bars_from_csvs({symbol: csvpath})

    def __iter__(self):
        """Iterate over the sorted bar data."""
        for bar in self.__bars:
            yield bar

