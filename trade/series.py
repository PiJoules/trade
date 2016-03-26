#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Data series used in a strategy.
"""


class Series(object):
    """Data series derived from another list or series."""

    def __init__(self, series, window_size=1, default=None):
        """
        Args:
            series (list): Series whose elements are used to calculate
                the elements of this series.
            window_size (Optional[int]): Window size of most recent elements
                to use in the given series to find the latest element of this
                series. Defaults to 1.
            default (Optional[Any]): Default value of an element in this
                series if the length of the base series is less than window
                size. Defaults to None.
        """
        assert window_size > 0

        self.__base_series = series
        self.__window_size = window_size
        self.__elems = []
        self.__default = default

    @property
    def data(self):
        return self.__elems

    @property
    def _window_size(self):
        return self.__window_size

    @property
    def _last(self):
        """Get the last element without updating this series."""
        return self.__elems[-1]

    def _new_elem(self, series):
        """Add a new elem to this series."""
        raise NotImplementedError

    def _first_elem(self, series):
        """Add a new elem to this series if this elem will be the first one."""
        raise NotImplementedError

    def __getitem__(self, key):
        """Get the nth element in this series."""
        # Cache vals
        base_series = self.__base_series
        window_size = self.__window_size
        elems = self.__elems
        default = self.__default

        # Make sure we are same size as base_series
        while len(elems) < len(base_series):
            if len(base_series) > window_size:
                # Adding new element
                elems.append(self._new_elem(base_series))
            elif len(base_series) < window_size:
                # Not enough elems in the base series.
                # Cannot calculate current elem without complete data.
                elems.append(default)
            else:
                # Finding first real element
                elems.append(self._first_elem(base_series))

        return elems[key]

