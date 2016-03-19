#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for handling the common file format to be used by the classes in this
module. The file type will be compressed jsonl.
"""

import gzip
import json


class JSONLWriter(object):
    """Class for writing compressed jsonl files."""

    def __init__(self, filename):
        self.__file = gzip.open(filename, "wb")

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_val, ex_tb):
        self.close()

    def close(self):
        self.__file.close()

    def writejson(self, json_obj):
        """Write a json object (list, dict) to the file."""
        self.__file.write(bytes(json.dumps(json_obj) + "\n", "UTF-8"))

