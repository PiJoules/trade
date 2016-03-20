#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Singleton representing the current state of the market visible
to everything.
"""

from .bar import Bar


class Market(object):
    """
    Current state of the market. The market will just keep track of the
    latest bar received, but total volume traded will be recorded.
    """

    __state = {}

    @staticmethod
    def update(bar):
        """Update the total_volume of trades."""
        symbol = bar.symbol
        state = Market.__state
        if symbol in state:
            state[symbol] = Bar.from_slot_defined_class(
                bar, volume=state[symbol].volume + bar.volume)
        else:
            state[symbol] = Bar.from_slot_defined_class(bar)

    @staticmethod
    def price(symbol):
        """Get the market price for a given symbol."""
        if symbol in Market.__state:
            return Market.__state[symbol].close
        return None

    @staticmethod
    def state(symbol):
        """Get the latest info for a given symbol."""
        return Market.__state.get(symbol, None)

