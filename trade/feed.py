#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for feeds that handle reading the compressed jsonl files.
"""

from .bar import Bar
from .jsonl import JSONLReader


class Feed(object):
    """Feed for reading compressed jsonl files."""

    def __init__(self, files=None):
        files = files or []
        self.__bars = []

    def add_files(self, files):
        """Add bar data from multiple files."""
        # Read jsonl file
        bars = []
        for filename in files:
            with JSONLReader(filename) as jsonl:
                for json_obj in jsonl:
                    bar = Bar(**json_obj)
                    bars.append(bar)

        # Add new bars and sort by receive time
        self.__bars = sorted(bars + self.__bars, key=lambda x: x.timestamp)

    def add_file(self, filename):
        """Add bar data from a single file."""
        self.add_files([filename])

    def __iter__(self):
        """Itrate over sorted bar data."""
        return iter(self.__bars)

