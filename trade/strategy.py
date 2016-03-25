#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for base strategy class.
"""

import logging

from .market import Market


class BaseStrategy(object):
    """Base class for strategies."""

    def __init__(self, broker=None, portfolio=None, silent=False,
                 streams=None):
        self.__broker = broker
        self.__portfolio = portfolio
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

    def run(self, feed):
        """Run the strategy through the feed."""
        broker = self.__broker
        portfolio = self.__portfolio
        for bar in feed:
            self.__datetime = bar.datetime

            # Update global market
            Market.update(bar)

            # Callbacks
            self.on_bar(bar)
            if broker and portfolio:
                broker.dispatch(portfolio, bar)

    @property
    def cash(self):
        """Total cash return."""
        raise NotImplemented

    @property
    def stock_value(self):
        """Totoal value of stocks only in USD."""
        raise NotImplemented

    @property
    def total_value(self):
        """Total value of cash and stocks in USD."""
        return self.cash + self.stock_value

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

