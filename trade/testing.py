#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for testing various values for a strategy to find the highest return.
"""

from itertools import product


def test_vals(strategy_cls, feed, *args, **kwargs):
    """Test various values as inputs for strategy."""
    # Records
    max_value = 0
    max_value_args = None

    # Split dict keys and iterable values into list of keys and
    # iterable vals where the association between key-value pairs
    # are maintained.
    if kwargs:
        kwarg_keys, kwarg_vals = list(zip(*list(kwargs.items())))
        kwarg_val_prod = product(*kwarg_vals)

    # For each possible combination of positional args.
    for args_ in product(*args):
        if kwargs:
            for kwarg_val_combo in kwarg_val_prod:
                # For each possible combination of keyword args
                kwargs_ = dict(zip(kwarg_keys, kwarg_val_combo))
                strategy = strategy_cls(*args_, **kwargs_)
                strategy.run(feed)
                total_value = strategy.total_value

                if total_value > max_value:
                    max_value_args = (args_, kwargs_)
                    max_value = total_value
        else:
            strategy = strategy_cls(*args_)
            strategy.run(feed)
            total_value = strategy.total_value

            if total_value > max_value:
                max_value_args = (args_, {})
                max_value = total_value

    return max_value, max_value_args

