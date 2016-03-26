#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for base strategy class.
"""

import logging
import sys

from .market import Market
from .broker import Broker


class BaseStrategy(object):
    """Base class for strategies."""

    def __init__(self, portfolio, feed, broker=None, silent=False,
                 files=None):
        self.__portfolio = portfolio
        self.__feed = feed
        self.__broker = broker or Broker()
        self.__datetime = None

        # Logger
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.DEBUG)
        if not silent:
            logger.addHandler(logging.StreamHandler(stream=sys.stdout))
        for f in files or []:
            logger.addHandler(logging.FileHandler(f, mode="w"))
        self.__logger = logger

    def run(self):
        """Run the strategy through the feed."""
        broker = self.__broker
        portfolio = self.__portfolio
        for bar in self.__feed:
            self.__datetime = bar.datetime

            # Update global market
            Market.update(bar)

            # Callbacks
            self.on_bar(bar)
            if broker and portfolio:
                errors = broker.dispatch(portfolio, bar)
                for error in errors:
                    self.error(error)

    ########################
    # Exposed properties
    ########################

    @property
    def _portfolio(self):
        return self.__portfolio

    @property
    def _broker(self):
        return self.__broker

    ########################
    # Logging methods
    ########################

    def __log(self, level, *args):
        args = map(str, args)
        self.__logger.debug(
            "{} {} [{}]: {}"
            .format(self.__datetime, self.__class__.__name__, level,
                    " ".join(args)))

    def debug(self, *args):
        self.__log("DEBUG", *args)

    def info(self, *args):
        self.__log("INFO", *args)

    def warn(self, *args):
        self.__log("WARNING", *args)

    def error(self, *args):
        self.__log("ERROR", *args)

    def critical(self, *args):
        self.__log("CRITICAL", *args)

    ########################
    # Callbak methods
    ########################

    def on_bar(self, bar):
        """Callback method for bars."""
        pass

