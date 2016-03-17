#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for base strategy class.
"""


class BaseStrategy(object):
    """Base class for strategies."""

    def run(self, feed):
        """Run the strategy through the feed."""
        for bar in feed:
            self.on_bar(bar)

    def on_bar(self, bar):
        """Callback method for bars."""
        pass

