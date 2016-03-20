#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for holding miscelanious data structures.
"""

from enum import Enum, unique
from datetime import datetime


class SlotDefinedClass(object):
    """Wrapper class for slotted classes."""

    __slots__ = tuple()
    __type_checks__ = {}  # Dict mapping attr => expected type
    __default_types__ = {}  # Dict mapping attr => default value for attr

    def __init__(self, *args, **kwargs):
        for attr in self.__slots__:
            if attr in kwargs:
                val = kwargs[attr]
            else:
                val = self.__default_types__[attr]

            if attr in self.__type_checks__:
                assert isinstance(val, self.__type_checks__[attr])

            setattr(self, attr, val)

    def __str__(self):
        return str({attr: getattr(self, attr) for attr in self.__slots__})

    def __hash__(self):
        return hash(tuple(getattr(self, attr) for attr in self.__slots__))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return not (self == other)


@unique
class TransactionType(Enum):
    """Class representing the different types of transactions."""

    BUY = 1
    SELL = 2
    SELL_SHORT = 3
    BUY_TO_COVER = 4


@unique
class PriceType(Enum):
    """Class for the different types of prices a broker can have."""

    MARKET = 1
    LIMIT = 2
    STOP = 3
    STOP_LIMIT = 4
    TRAILING_STOP = 5


@unique
class Duration(Enum):
    """Class for the different types of duration for orders."""

    GOOD_TIL_CANCELLED = 1
    DAY_ORDER = 2


class Order(SlotDefinedClass):
    """Class representing a trade order."""

    __slots__ = ("symbol", "transaction", "volume", "price", "price_type",
                 "duration", "timestamp")
    __type_checks__ = {
        "price_type": PriceType,
        "duration": Duration,
        "transaction": TransactionType
    }
    __default_types__ = {
        "price_type": PriceType.MARKET,
        "duration": Duration.GOOD_TIL_CANCELLED,
        "timestamp": datetime.now().timestamp()
    }


class Stock(SlotDefinedClass):
    """Class representing a share in a company."""

    __slots__ = ("symbol", "timestamp", "volume")

    @classmethod
    def from_order(cls, order):
        assert isinstance(order, Order)
        return cls(symbol=order.symbol,
                   timestamp=order.timestamp,
                   volume=order.volume)

    def __add__(self, other):
        """
        Add the volumes for the 2 stocks.
        timestamp will be the one of the latest order.
        """
        assert self.symbol == other.symbol
        return Stock(symbol=self.symbol,
                     timestamp=max(self.timestamp, other.timestamp),
                     volume=self.volume + other.volume)

    def __iadd__(self, other):
        assert self.symbol == other.symbol
        self.timestamp = max(self.timestamp, other.timestamp)
        self.volume += other.volume

    def __sub__(self, other):
        assert self.symbol == other.symbol
        return Stock(symbol=self.symbol,
                     timestamp=max(self.timestamp, other.timestamp),
                     volume=self.volume - other.volume)

    def __isub__(self, other):
        assert self.symbol == other.symbol
        self.timestamp = max(self.timestamp, other.timestamp)
        self.volume -= other.volume

