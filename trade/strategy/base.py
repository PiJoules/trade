#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for base strategy class.
"""


class BaseStrategy(object):
    """Base class for strategies."""

    def __init__(self, data_feed, broker):
        self.__data_feed = data_feed

