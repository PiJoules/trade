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
        self.__pending_orders = {}
        self.__transactions = {}
        self.__order_count = 0  # Total number of orders made
        self.__errors = []  # Error messages

    ##############################
    # Exposed properties
    ##############################

    @property
    def transactions(self):
        return self.__transactions

    @property
    def pending_orders(self):
        return self.__pending_orders

    ##############################
    # Public order methods
    ##############################

    def place(self, order):
        """Handle an order and return the order_id."""
        assert isinstance(order, Order)
        order_id = self.__order_count
        self.__pending_orders[order_id] = order
        self.__order_count = order_id + 1
        return order_id

    def buy(self, bar, volume):
        """Place a BUY order."""
        self.place(Order(symbol=bar.symbol,
                         volume=volume,
                         price=bar.close,
                         transaction=TransactionType.BUY,
                         timestamp=bar.timestamp))

    def sell(self, bar, volume):
        """Place a SELL order."""
        self.place(Order(symbol=bar.symbol,
                         volume=volume,
                         price=bar.close,
                         transaction=TransactionType.SELL,
                         timestamp=bar.timestamp))

    def cancel(self, order_id):
        """Cancel a pening order."""
        del self.__pending_orders[order_id]

    ##############################
    # Private order methods
    ##############################

    def __buy(self, order, portfolio):
        """Remove cash from portfolio. Add stocks."""
        amount = order.price * order.volume
        if not portfolio.withdraw_cash(amount):
            self.__errors.append(
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
        Should be called only by strategy in run() method.

        TODO: Add some form of randomness to replicate the market more.
        - Delayed time in executing the trade.
        - Unable to find buyer/seller for order.
        """
        transactions = self.__transactions
        pending_orders = self.__pending_orders
        self.__errors.clear()

        # Try to execute pending orders
        for order_id, order in sorted(pending_orders.items()):
            transaction = order.transaction
            executed = False

            if transaction == TransactionType.BUY:
                executed = self.__buy(order, portfolio)
            elif transaction == TransactionType.SELL:
                executed = self.__sell(order, portfolio)
            elif transaction == TransactionType.SELL_SHORT:
                executed = self.__sell_short(order, portfolio)
            elif transaction == TransactionType.BUY_TO_COVER:
                executed = self.__buy_to_cover(order, portfolio)
            else:
                raise Exception(
                    "Unknown transaction type '{}': allowed '{}'"
                    .format(transaction, list(TransactionType)))

            if executed:
                transactions[order_id] = order
                del pending_orders[order_id]

        return self.__errors

