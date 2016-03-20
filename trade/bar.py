#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for static types.
"""

from datetime import datetime


class Frequency(object):
    """Enum for frequencies."""

    TRADE = -1
    SECOND = 1
    MINUTE = 60
    HOUR = 60 * 60
    DAY = 24 * 60 * 60
    WEEK = 24 * 60 * 60 * 7
    MONTH = 24 * 60 * 60 * 31


class Bar(object):
    """Class represnting a row of data."""

    __slots__ = ("timestamp", "open", "high", "low", "close", "volume",
                 "adjusted_close", "symbol")

    def __init__(self, **kwargs):
        open_ = kwargs["open"]
        high = kwargs["high"]
        low = kwargs["low"]
        close = kwargs["close"]
        timestamp = kwargs["timestamp"]

        # Check params
        if high < low:
            raise Exception("high < low at '{}'".format(timestamp))
        if high < open_:
            raise Exception("high < open at '{}'".format(timestamp))
        if high < close:
            raise Exception("high < close at '{}'".format(timestamp))
        if low > open_:
            raise Exception("low > open at '{}'".format(timestamp))
        if low > close:
            raise Exception("low > close at '{}'".format(timestamp))

        self.timestamp = timestamp
        self.open = open_
        self.high = high
        self.low = low
        self.close = close
        self.volume = kwargs["volume"]
        self.adjusted_close = kwargs.get("adj_close", None)
        self.symbol = kwargs["symbol"]

    @property
    def datetime(self):
        return datetime.fromtimestamp(self.timestamp)

    def __str__(self):
        return str({attr: getattr(self, attr) for attr in self.__slots__})

