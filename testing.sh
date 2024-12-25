#!/bin/bash

set -o errexit

echo "unit tests:"
python -m unittest
