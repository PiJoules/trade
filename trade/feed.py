#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for feeds that handle reading the compressed jsonl files.
"""

from .bar import Bar
from .jsonl import JSONLReader


class Feed(object):
    """Feed for reading compressed jsonl files."""

    def __init__(self, *args, buffer_size=None):
        assert len(args) > 0
        self.__readers = [JSONLReader(f) for f in args]
        self.__buffer_size = buffer_size
        self.__buffer = None if buffer_size is None else []
        #self.__files = []
        #self.__bars = []

    #def add_files(self, files):
    #    """Add bar data from multiple files."""
    #    # Read jsonl file
    #    bars = []
    #    for filename in files:
    #        with JSONLReader(filename) as jsonl:
    #            for json_obj in jsonl:
    #                bar = Bar(**json_obj)
    #                bars.append(bar)

    #    # Add new bars and sort by receive time
    #    self.__bars = sorted(bars + self.__bars, key=lambda x: x.timestamp)

    #def add_file(self, filename):
    #    """Add bar data from a single file."""
    #    self.add_files([filename])

    @property
    def buffer(self):
        """Cached buffer of the most recent bars."""
        return self.__buffer

    def __iter__(self):
        """Itrate over sorted bar data."""
        #return iter(self.__bars)
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
            yield bar_obj
            if buff is not None:
                buff.append(bar_obj)
                if len(buff) > buff_size:
                    buff.pop(0)

            # Get the next bar and replace the yielded bar with it.
            # If there are no more bars in that reader, remove the
            # iterator and close the reader.
            next_bar = next(readers[min_index], None)
            if next_bar is None:
                del bars[min_index]
                readers[min_index].close()
            else:
                bars[min_index] = next_bar

