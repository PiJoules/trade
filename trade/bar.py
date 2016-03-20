#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for static types.
"""

from .data import SlotDefinedClass
from datetime import datetime


class Bar(SlotDefinedClass):
    """Class represnting a row of data."""

    __slots__ = ("timestamp", "open", "high", "low", "close", "volume",
                 "adjusted_close", "symbol")
    __default_types__ = {
        "adjusted_close": None
    }

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

        super().__init__(**kwargs)

    @property
    def datetime(self):
        return datetime.fromtimestamp(self.timestamp)

