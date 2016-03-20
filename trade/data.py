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

    def __init__(self, **kwargs):
        for attr in self.__slots__:
            if attr in kwargs:
                val = kwargs[attr]
            else:
                val = self.__default_types__[attr]

            if attr in self.__type_checks__:
                assert isinstance(val, self.__type_checks__[attr])

            setattr(self, attr, val)

    @classmethod
    def from_slot_defined_class(cls, sdc, **kwargs):
        """
        Create a copy of a SlotDefinedClass from a SlotDefinedClass.

        Args:
            sdc (SlotDefinedClass): Object whose attributes and values will
                be copied to the new object.
            **kwargs: Arbitrary keyword arguments. Values for keys provided
                here will override that provided for the same key in sdc.
        """
        assert isinstance(sdc, cls)
        state = sdc.dict()
        state.update(kwargs)
        return cls(**state)

    def dict(self):
        """Create a dict from a SlotDefinedClass."""
        return {attr: getattr(self, attr) for attr in self.__slots__}

    def __str__(self):
        return str(self.dict())

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

