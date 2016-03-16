#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for the yahoo finance data feed.
"""

from trade import bar


class YahooFeed(object):
    """Class for handling data downloaded from yahoo finance."""

    def __init__(self, freq=bar.Frequency.DAY, timezone=None, max_len=1024):
        pass

