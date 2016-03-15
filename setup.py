#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


def long_description():
    with open("README.md", "r") as readme:
        return readme.read()


def packages():
    return find_packages(include=["trade*"])


def install_requires():
    with open("requirements.txt", "r") as requirements:
        return requirements.readlines()


setup(
    name="trade",
    version="0.0.1",
    description="Backtesting module",
    long_description=long_description(),
    #url=None,
    author="Leonard Chan",
    author_email="lchan1994@yahoo.com",
    license="Unlicense",
    classifiers=[
        "Development Status :: 3 - Alpha",
    ],
    keywords="backtest",
    packages=packages(),
    install_requires=install_requires(),
    entry_points={
        "console_scripts": [
            "download_yahoo_daily=trade.tools.yahoo:download_daily",
        ]
    }
)

