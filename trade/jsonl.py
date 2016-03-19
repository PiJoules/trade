#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for handling the common file format to be used by the classes in this
module. The file type will be compressed jsonl.
"""

import gzip
import json


class JSONLFile(object):
    """Class for handling compressed jsonl files."""

    def __init__(self, file_):
        self._file = file_

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_val, ex_tb):
        self.close()

    def close(self):
        self._file.close()


class JSONLWriter(JSONLFile):
    """Class for writing compressed jsonl files."""

    def __init__(self, filename):
        super().__init__(gzip.open(filename, "wb"))

    def writejson(self, json_obj):
        """Write a json object (list, dict) to the file."""
        self._file.write(bytes(json.dumps(json_obj) + "\n", "UTF-8"))


class JSONLReader(JSONLFile):
    """Class for reading compressed jsonl files."""

    def __init__(self, filename):
        super().__init__(gzip.open(filename, "rb"))

    def readjson(self):
        """Read a line from the jsonl file."""
        return json.loads(self._file.readline().decode("utf-8"))

    def __iter__(self):
        for line in self._file:
            yield json.loads(line.decode("utf-8"))

