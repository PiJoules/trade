#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for the yahoo finance data feed.
"""

from trade import bar


class RowParser(object):



class YahooFeed(object):
    """Class for handling data downloaded from yahoo finance."""

    def __init__(self, freq=bar.Frequency.DAY, timezone=None, max_len=1024):
        super(YahooFeed, self).__init__(freq, max_len)
        self.__timezone = timezone
        self.__sanitize_bars = False

    def add_data_from_csv(self, symbol, csvpath):
        """Load data from a csv from yahoo finance."""
        parser = RowParser(self.daily_data_time, self.frequency,
                           self.__timezonem, self.__sanitize_bars)
        self.add_data_from_csv(symbol, csvpath, parser)

