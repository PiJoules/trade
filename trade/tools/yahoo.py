#!/usr/bin/env python

"""
Module for downloading bar data from yahoo finance endpoints
and converting them to compressed jsonl files.
"""

from datetime import date, datetime
from argparse import ArgumentParser
from .csv import download_csv
from ..jsonl import JSONLWriter

YAHOO_BASE = "http://ichart.finance.yahoo.com/table.csv"
YAHOO_INTRA_DAY = ("http://chartapi.finance.yahoo.com/instrument/1.0/"
                   "{symbol}/chartdata;type=quote;range=1d/csv")


def download_daily_data(symbol, year, output):
    """
    Download daily stock data for a given stock symbol over 1 year.

    Format:
    Date,Open,High,Low,Close,Volume,Adj Close
    2000-12-29,30.875,31.3125,28.6875,29.0625,31702200,26.989868
    2000-12-28,30.5625,31.625,30.375,31.0625,25053600,28.847236
    2000-12-27,30.375,31.0625,29.375,30.6875,26437500,28.498979
    ...
    """
    start = date(year, 1, 1)
    end = date(year, 12, 31)
    csv_text = download_csv(YAHOO_BASE, params={
        "s": symbol,
        "a": start.month - 1,
        "b": start.day,
        "c": start.year,
        "d": end.month - 1,
        "e": end.day,
        "f": end.year,
        "g": "d",
        "ignore": ".csv"
    })
    csv_lines = csv_text.split("\n")

    # Check types
    assert csv_lines[0] == "Date,Open,High,Low,Close,Volume,Adj Close"

    # Format lines to common jsonl spec
    with JSONLWriter(output) as jsonl:
        for line in csv_lines[1:]:
            line = line.strip()
            if not line:
                continue
            row = line.split(",")

            # Local datetime as seconds since epoch
            recv_time = datetime.strptime(row[0], "%Y-%m-%d").timestamp()
            jsonl.writejson({
                "timestamp": recv_time,
                "open": float(row[1]),
                "high": float(row[2]),
                "low": float(row[3]),
                "close": float(row[4]),
                "volume": int(row[5]),
                "adj_close": float(row[6]),
                "symbol": symbol
            })


def download_intra_day_data(symbol, output):
    """
    Download intra day stock data for the last trading day.

    Format:
    uri:/instrument/1.0/GOOG/chartdata;type=quote;range=1d/csv
    ticker:goog
    Company-Name:Alphabet Inc.
    Exchange-Name:NMS
    unit:MIN
    timezone:EDT
    currency:USD
    gmtoffset:-14400
    previous_close:737.7800
    Timestamp:1458307800,1458331200
    labels:1458309600,1458313200,1458316800,1458320400,1458324000,1458327600,1458331200
    values:Timestamp,close,high,low,open,volume
    close:732.2100,739.9100
    high:732.5300,740.2700
    low:731.8800,739.9100
    open:732.0200,739.9800
    volume:100,550800
    1458307830,739.4700,739.4800,739.4500,739.4500,550800
    1458307868,739.9100,740.0600,739.9100,739.9500,4300
    1458307925,739.4500,740.2500,739.2500,739.9800,4800
    1458307984,739.8100,739.8300,738.8915,739.0000,11900
    1458308066,739.6300,740.2700,739.6300,739.7900,6200
    ...
    """
    url = YAHOO_INTRA_DAY.format(symbol=symbol)
    csv_text = download_csv(url, content_type="text/plain; charset=utf-8")
    csv_lines = csv_text.split("\n")

    # Check types
    assert csv_lines[1] == ("ticker:" + symbol.lower())
    assert csv_lines[11] == "values:Timestamp,close,high,low,open,volume"

    # Format lines to common jsonl spec
    with JSONLWriter(output) as jsonl:
        for line in csv_lines[17:]:
            line = line.strip()
            if not line:
                continue
            row = line.split(",")
            jsonl.writejson({
                "timestamp": int(row[0]),
                "close": float(row[1]),
                "high": float(row[2]),
                "low": float(row[3]),
                "open": float(row[4]),
                "volume": int(row[5]),
                "symbol": symbol
            })


"""
Console scripts.
"""


def download_daily():
    """Cmd line function for calling download_yahoo_csv."""
    parser = ArgumentParser("Download Yahoo daily data")
    parser.add_argument("symbol", help="Stock symbol.")
    parser.add_argument("year", type=int,
                        help="Year in format YYYY.")
    parser.add_argument("output", help="Output file to write compressed "
                        "jsonl to.")
    args = parser.parse_args()
    download_daily_data(args.symbol, args.year, args.output)


def download_intra_day():
    """Cmd line function for calling download_yahoo_csv."""
    parser = ArgumentParser("Download Yahoo intra day data")
    parser.add_argument("symbol", help="Stock symbol.")
    parser.add_argument("output", help="Output file to write compressed "
                        "jsonl to.")
    args = parser.parse_args()
    download_intra_day_data(args.symbol, args.output)

