#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages

STRATEGIES_DIR = "strategies"


def long_description():
    with open("README.md", "r") as readme:
        return readme.read()


def packages():
    return find_packages(include=["trade*", "strategies*"])


def install_requires():
    with open("requirements.txt", "r") as requirements:
        return requirements.readlines()


def strategy_scripts():
    if not os.path.isdir(STRATEGIES_DIR):
        return

    for strategy in os.listdir(STRATEGIES_DIR):
        # Ignore __init__.py in strategies
        if strategy in ("__init__.py", "__pycache__", "__init__.pyc"):
            continue

        scripts_path = os.path.join(STRATEGIES_DIR, strategy, "scripts")
        for script_name in os.listdir(scripts_path):
            if script_name.endswith(".py") and script_name != "__init__.py":
                module = ".".join([STRATEGIES_DIR, strategy, "scripts",
                                   script_name[:-3]])
                script_name = strategy + "_" + script_name[:-3]
                yield script_name + "=" + module + ":main"


setup(
    name="trade",
    version="0.0.1",
    description="Backtesting module",
    long_description=long_description(),
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
    test_suite="tests",
    entry_points={
        "console_scripts": [
            "plot_intra_day=trade.plot:main",
            "download_yahoo_daily=trade.tools.yahoo:download_daily",
            "download_yahoo_intra_day=trade.tools.yahoo:download_intra_day",
        ] + list(strategy_scripts())
    }
)

