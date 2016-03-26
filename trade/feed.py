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
        self.__buffer_size = 0
        self.__buffer = None
        self.__length = 0

    def use_buffer(self, buffer_size):
        """Let the last bars be available in a buffer."""
        self.__buffer_size = buffer_size
        if self.__buffer is None:
            self.__buffer = []

    def reset(self):
        """Reset the readers and buffer."""
        for reader in self.__readers:
            reader.reset()
        if self.__buffer is not None:
            self.__buffer.clear()
        self.__length = 0

    def __len__(self):
        """Number of bars yielded."""
        return self.__length

    def __getitem__(self, key):
        """Get the nth element of the buffer."""
        return self.__buffer[key]

    def __iter__(self):
        """Itrate over sorted bar data."""
        buff = self.__buffer
        buff_size = self.__buffer_size

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
            self.__length += 1
            if buff is not None:
                buff.append(bar_obj)
                if len(buff) > buff_size:
                    buff.pop(0)
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

