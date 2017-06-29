#!/bin/bash

set -e

rm -rf dist
python setup.py -q sdist bdist_wheel
twine upload dist/*

echo "Now run 'git tag <version>'"
