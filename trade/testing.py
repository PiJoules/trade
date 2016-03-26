#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for testing various values for a strategy to find the highest return.
"""

from itertools import product
from collections import Iterable


def test_vals(strategy_cls, feed, *args, **kwargs):
    """Test various values as inputs for strategy."""
    # Results
    max_results = {
        "value": 0,
        "args": None
    }

    # Place any non-iterable args and kwargs in lists.
    # These are arguments that do not neet to be tested for.
    args = [arg if isinstance(arg, Iterable) else [arg] for arg in args]
    kwargs = {k: (v if isinstance(v, Iterable) else [v])
              for k, v in kwargs.items()}

    # Split dict keys and iterable values into list of keys and
    # iterable vals where the association between key-value pairs
    # are maintained.
    if kwargs:
        kwarg_keys, kwarg_vals = list(zip(*list(kwargs.items())))

    def run_strategy(args_, kwargs_=None):
        kwargs_ = kwargs_ or {}
        feed.reset()
        if kwargs_:
            strategy = strategy_cls(feed, *args_, **kwargs_)
        else:
            strategy = strategy_cls(feed, *args_)
        strategy.run()
        total_value = strategy.total_value

        if total_value > max_results["value"]:
            max_results["args"] = (args_, kwargs_)
            max_results["value"] = total_value

    # For each possible combination of positional args.
    for args_ in product(*args):
        if kwargs:
            for kwarg_val_combo in product(*kwarg_vals):
                # For each possible combination of keyword args
                kwargs_ = dict(zip(kwarg_keys, kwarg_val_combo))
                run_strategy(args_, kwargs_)
        else:
            run_strategy(args_)

    return max_results["value"], max_results["args"]

