#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
- If the close price is above the SMA(20) we enter a long position
  (we place a buy market order).
- If a long position is in place, and the close price drops below
  the SMA(20) we exit the long position (we place a sell market order).
"""

from trade import Portfolio, Order, TransactionType, BaseStrategy, Series
from statistics import mean


class SMASeries(Series):
    """Simple moving average series."""

    def _first_elem(self, base_series):
        """
        Only take the collective sum once.
        The length of the series will be the same as the window size.
        """
        return mean(base_series)

    def _new_elem(self, base_series):
        """
        Add the new elem and subtract the oldest elem.
        The length of the series will be greater than the window_size.
        """
        window_size = self._window_size
        return (self._last + (base_series[-1] / window_size) -
                (base_series[-1 - window_size] / window_size))


class SMAStrategy(BaseStrategy):

    def __init__(self, feed, window_size, cash, **kwargs):
        super().__init__(Portfolio(cash=cash), feed, **kwargs)
        #self.__window = []
        #self.__window_size = window_size
        self.__sma = SMASeries(feed.buffer)

    @property
    def total_value(self):
        return self._portfolio.total_value

    def buy(self, bar, sma, amount):
        order = Order(symbol=bar.symbol,
                      volume=amount,
                      price=bar.close,
                      transaction=TransactionType.BUY,
                      timestamp=bar.timestamp)
        self._broker.place(order)
        self.info("BUY at ${:.2f} (balance ${:.2f})"
                  .format(bar.close, self._portfolio.cash))

    def sell(self, bar, sma, amount):
        order = Order(symbol=bar.symbol,
                      volume=amount,
                      price=bar.close,
                      transaction=TransactionType.SELL,
                      timestamp=bar.timestamp)
        self._broker.place(order)
        self.info("SELL at ${:.2f} (balance ${:.2f})"
                  .format(bar.close, self._portfolio.cash))

    def on_bar(self, bar):
        #window = self.__window
        #window.append(bar.close)
        #window_size = self.__window_size
        #sma = None
        #if len(window) > window_size:
        #    del window[0]
        #if len(window) == window_size:
        #    sma = sum(window) / window_size
        sma = self.__sma[-1]
        if sma is None:
            return

        if (not self._portfolio.contains_symbol(bar.symbol) and
                bar.close > sma):
            self.buy(bar, sma, 10)
        elif (self._portfolio.contains_symbol(bar.symbol) and
                bar.close < sma):
            self.sell(bar, sma, 10)

