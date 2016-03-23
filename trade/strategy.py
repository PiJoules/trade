#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for base strategy class.
"""

from .market import Market


class BaseStrategy(object):
    """Base class for strategies."""

    def __init__(self, broker=None, portfolio=None):
        self.__broker = broker
        self.__portfolio = portfolio

    def run(self, feed):
        """Run the strategy through the feed."""
        broker = self.__broker
        portfolio = self.__portfolio
        for bar in feed:
            Market.update(bar)
            self.on_bar(bar)
            if broker and portfolio:
                broker.dispatch(portfolio, bar)

    def on_bar(self, bar):
        """Callback method for bars."""
        pass

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


