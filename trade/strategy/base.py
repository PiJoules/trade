#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for base strategy class.
"""

from ..broker import Broker
from ..portfolio import Portfolio


class BaseStrategy(object):
    """Base class for strategies."""

    def __init__(self, broker, portfolio):
        assert isinstance(broker, Broker)
        assert isinstance(portfolio, Portfolio)

        self.__broker = broker
        self.__portfolio = portfolio

    def run(self, feed):
        """Run the strategy through the feed."""
        for bar in feed:
            self.on_bar(bar)
            self.__broker.dispatch(self.__portfolio, bar)

    def on_bar(self, bar):
        """Callback method for bars."""
        pass

