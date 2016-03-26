#!/usr/bin/env sh

rm -rf build/ dist/ *.egg-info/ __pycache__

dirs_to_check="trade/ strategies/"
for d in $dirs_to_check; do
    find $d -name '*.pyc' -exec rm {} \;
    find $d -name '__pycache__' -type d -exec rm -rf {} \;
done

