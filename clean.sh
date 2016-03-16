#!/usr/bin/env sh

rm -rf build/ dist/ *.egg-info/
find trade/ -name '*.pyc' -exec rm {} \;
find trade/ -name '__pycache__' -type d -exec rm -rf {} \;

