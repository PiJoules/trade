#!/usr/bin/env python

"""
Module for handing csvs.
"""

import requests


def download_csv(url, params=None, content_type="text/csv"):
    """Wrapper function for downloading a csv."""
    # Make request and get response
    resp = requests.get(url, params=params)

    # Check response
    resp.raise_for_status()
    resp_content_type = resp.headers["content-type"]
    if resp_content_type != content_type:
        raise Exception("Invalid content-type: {}".format(resp_content_type))

    # Remove byte order mark
    text = resp.text
    while not text[0].isalnum():
        text = text[1:]

    return text

