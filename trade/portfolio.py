#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for the portfolio which contains the user's financial assets.
"""

from .market import Market
from collections import defaultdict


class Portfolio(object):
    """Class for holding assets avaialble for trading by the broker."""

    def __init__(self, cash=0, stocks=None):
        """
        Args:
            cash (Optional[int]): Starting cash. Defaults to 0.
            stocks (Optional[Dict[str, int]): Starting stocks.
                Defaults to None.
        """
        self.__cash = cash
        self.__stocks = defaultdict(int, stocks or {})

    @property
    def cash(self):
        """Cash in portfolio."""
        return self.__cash

    @property
    def stocks(self):
        """All stocks in portfolio."""
        return self.__stocks

    @property
    def stock_value(self):
        """Cash value of all stocks in portfolio."""
        return sum(Market.price(symbol) * volume
                   for symbol, volume in self.__stocks.items())

    @property
    def total_value(self):
        """Total cash value of portfolio."""
        return self.cash + self.stock_value

    def contains_symbol(self, symbol):
        """If the portfolio contains shares for a given company."""
        return bool(self.__stocks[symbol])

    def add_cash(self, cash):
        """Add more money to be traded."""
        self.__cash += cash

    def withdraw_cash(self, cash):
        """Remove money to be open for trading."""
        if cash > self.__cash:
            return False
        self.__cash -= cash
        return True

    def add_stock(self, symbol, volume):
        self.__stocks[symbol] += volume

    def remove_stock(self, symbol, volume):
        stocks = self.__stocks
        if symbol not in stocks:
            raise Exception("'{}' was not purchased before.".format(symbol))
        if volume > stocks[symbol]:
            raise Exception(
                ("Attempted to remove more shares for '{}' from portfolio:"
                 "removing {}, current {}")
                .format(symbol, volume, stocks[symbol]))
        stocks[symbol] -= volume

