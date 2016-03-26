#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for base strategy class.
"""

import logging

from .market import Market
from .broker import Broker


class BaseStrategy(object):
    """Base class for strategies."""

    def __init__(self, portfolio, feed, broker=None, silent=False, streams=None):
        self.__portfolio = portfolio
        self.__feed = feed
        self.__broker = broker or Broker()
        self.__datetime = None

        # Logger
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logging.StreamHandler())
        streams = streams or []
        for stream in streams:
            logger.addHandler(stream=stream)
        self.__logger = logger

        # Do not print output
        if silent:
            logger.handlers = []

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

    def debug(self, msg):
        self.__logger.debug(
            "{} {} [DEBUG]: {}"
            .format(self.__datetime, self.__class__.__name__, msg))

    def info(self, msg):
        self.__logger.debug(
            "{} {} [INFO]: {}"
            .format(self.__datetime, self.__class__.__name__, msg))

    def warn(self, msg):
        self.__logger.debug(
            "{} {} [WARNING]: {}"
            .format(self.__datetime, self.__class__.__name__, msg))

    def error(self, msg):
        self.__logger.debug(
            "{} {} [ERROR]: {}"
            .format(self.__datetime, self.__class__.__name__, msg))

    def critical(self, msg):
        self.__logger.debug(
            "{} {} [CRITICAL]: {}"
            .format(self.__datetime, self.__class__.__name__, msg))

    ########################
    # Callbak methods
    ########################

    def on_bar(self, bar):
        """Callback method for bars."""
        pass

