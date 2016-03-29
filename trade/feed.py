#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for feeds that handle reading the compressed jsonl files.
"""

from .bar import Bar
from .jsonl import JSONLReader


class Feed(object):
    """Feed for reading compressed jsonl files."""

    def __init__(self, *args):
        assert len(args) > 0
        self.__readers = [JSONLReader(f) for f in args]
        self.__buffer = []

    def reset(self):
        """Reset the readers and buffer."""
        for reader in self.__readers:
            reader.reset()
        self.__buffer.clear()

    def __len__(self):
        """Number of bars yielded."""
        return len(self.__buffer)

    def __getitem__(self, key):
        """Get the nth element of the buffer."""
        return self.__buffer[key]

    def __iter__(self):
        """Itrate over sorted bar data."""
        buff = self.__buffer

        # Create iterators
        readers = [iter(x) for x in self.__readers]

        # Keep a dict to store the bars that weren't yielded, and on the
        # next iteration, replace the yielded bar with one from the reader that
        # bar came from.
        bars = {i: next(x, None) for i, x in enumerate(readers)}

        # Remove any Nones
        bars = {k: v for k, v in bars.items() if v is not None}

        # On each iteration, yield the earliest bar.
        while bars:
            # Get bar with smallest timestamp and yield it
            min_index, bar = min(bars.items(), key=lambda x: x[1]["timestamp"])
            bar_obj = Bar(**bar)
            buff.append(bar_obj)
            yield bar_obj

            # Get the next bar and replace the yielded bar with it.
            # If there are no more bars in that reader, remove the
            # iterator and close the reader.
            next_bar = next(readers[min_index], None)
            if next_bar is None:
                del bars[min_index]
                readers[min_index].close()
            else:
                bars[min_index] = next_bar

