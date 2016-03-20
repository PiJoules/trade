#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for broker who will handle buying and selling for us.

The broker will be able to perform the following transactions:
- Buy
- Sell
- Sell short
- Buy to cover (short)

The broker will be able to transact with the following price types:
- Market
- Limit
- Stop
- Stop-Limit
- Trailing stop ($ or %)
  - Dollar or percentage amount above/below current MARKET price.
  - Same as stop, but a percentage can be used.
  - Triggered relative to the MARKET price (not transaction price).

The pending order (while no transaction has taken place) will be open for
the following durations:
- Good Til Cancelled
- Day Order
"""

import logging

from .data import Order, TransactionType

LOGGER = logging.getLogger(__name__)


class Broker(object):
    """Class representing the intermediary in charge of trading for us."""

    def __init__(self):
        self.__pending_orders = set()
        self.__transactions = set()

    @property
    def transactions(self):
        return self.__transactions

    @property
    def pending_orders(self):
        return self.__pending_orders

    def place(self, order):
        """Handle an order."""
        assert isinstance(order, Order)
        self.__pending_orders.add(order)

    def cancel(self, order):
        """Cancel a pening order."""
        assert isinstance(order, Order)
        self.__pending_orders.remove(order)

    def __buy(self, order, portfolio):
        """Remove cash from portfolio. Add stocks."""
        amount = order.price * order.volume
        if not portfolio.withdraw_cash(amount):
            LOGGER.warning(
                "Not enough money to withdraw from portfolio: "
                "total order amount '{}', portfolio cash '{}'"
                .format(amount, portfolio.cash))
            return False

        portfolio.add_stock(order.symbol, order.volume)
        return True

    def __sell(self, order, portfolio):
        """Remove stocks from portfolio. Add cash."""
        amount = order.price * order.volume
        portfolio.remove_stock(order.symbol, order.volume)
        portfolio.add_cash(amount)
        return True

    def __sell_short(self, order, portfolio):
        """TODO: Implement"""
        raise NotImplemented

    def __buy_to_cover(self, order, portfolio):
        """TODO: Implement"""
        raise NotImplemented

    def dispatch(self, portfolio, bar):
        """
        Check for available orders to execute.

        TODO: Add some form of randomness to replicate the market more.
        - Delayed time in executing the trade.
        - Unable to find buyer/seller for order.
        """
        completed_orders = set()
        for order in self.__pending_orders:
            transaction = order.transaction

            if transaction == TransactionType.BUY:
                if self.__buy(order, portfolio):
                    completed_orders.add(order)
            elif transaction == TransactionType.SELL:
                if self.__sell(order, portfolio):
                    completed_orders.add(order)
            elif transaction == TransactionType.SELL_SHORT:
                if self.__sell_short(order, portfolio):
                    completed_orders.add(order)
            elif transaction == TransactionType.BUY_TO_COVER:
                if self.__buy_to_cover(order, portfolio):
                    completed_orders.add(order)
            else:
                raise Exception(
                    "Unknown transaction type '{}': allowed '{}'"
                    .format(transaction, list(TransactionType)))

        # Record completed transactions
        for order in completed_orders:
            self.__pending_orders.remove(order)
            self.__transactions.add(order)

