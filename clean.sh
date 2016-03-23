#!/usr/bin/env sh

rm -rf build/ dist/ *.egg-info/ tests/outputs/ __pycache__
find trade/ -name '*.pyc' -exec rm {} \;
find trade/ -name '__pycache__' -type d -exec rm -rf {} \;
find tests/ -name '*.pyc' -exec rm {} \;
find tests/ -name '__pycache__' -type d -exec rm -rf {} \;

