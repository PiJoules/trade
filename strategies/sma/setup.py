#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This should be called from the root of the repo.
"""

from setuptools import setup, find_packages


def packages():
    return find_packages(include=["trade*", "strategies.sma*"])


def install_requires():
    with open("requirements.txt", "r") as requirements:
        return requirements.readlines()


setup(
    name="sma",
    version="0.0.1",
    description="SMA trading strategy",
    url="https://github.com/PiJoules/trade",
    author="Leonard Chan",
    author_email="lchan1994@yahoo.com",
    license="Unlicense",
    classifiers=[
        "Development Status :: 3 - Alpha",
    ],
    keywords="backtest",
    packages=packages(),
    install_requires=install_requires(),
    test_suite="strategies.sma.tests",
    entry_points={
        "console_scripts": [
            "sma_backtest=strategies.sma.scripts.backtest:main",
            "sma_ideal=strategies.sma.scripts.ideal:main",
            "plot_intra_day=trade.plot:main",
            "download_yahoo_daily=trade.tools.yahoo:download_daily",
            "download_yahoo_intra_day=trade.tools.yahoo:download_intra_day",
        ]
    }
)

