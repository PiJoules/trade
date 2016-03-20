#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for the portfolio which contains the user's financial assets.
"""


class Portfolio(object):
    """Class for holding assets avaialble for trading by the broker."""

    def __init__(self, cash=0, stocks=None):
        self.__cash = cash
        self.__stocks = stocks or {}

    @property
    def cash(self):
        return self.__cash

    @property
    def stocks(self):
        return self.__stocks

    def contains_symbol(self, symbol):
        """If the portfolio contains shares for a given company."""
        return symbol in self.__stocks

    def add_cash(self, cash):
        """Add more money to be traded."""
        self.__cash += cash

    def withdraw_cash(self, cash):
        """Remove money to be open for trading."""
        if cash > self.__cash:
            return False
        self.__cash -= cash
        return True

    def add_stock(self, stock):
        stocks = self.__stocks
        symbol = stock.symbol
        if symbol not in stocks:
            stocks[symbol] = stock
        else:
            stocks[symbol] += stock

    def remove_stock(self, stock):
        stocks = self.__stocks
        symbol = stock.symbol
        if symbol not in stocks:
            raise Exception("'{}' was not purchased before.".format(symbol))
        if stock.volume > stocks[symbol].volume:
            raise Exception(
                ("Attempted to remove more shares for '{}' from portfolio:"
                 "removing {}, current {}")
                .format(symbol, stock.volume, stocks[symbol].volume))
        stocks[symbol] -= stock
        if not stocks[symbol]:
            del stocks[symbol]

