#!/bin/bash

echo "main code coding style check:"
pylint --recursive=y --rcfile=./src/.pylintrc --fail-under=10.0 src
black --check --diff src
isort --check --diff --profile black src

echo "test code coding style check:"
pylint --recursive=y --rcfile=./tests/.pylintrc --fail-under=10.0 tests
black --check --diff tests
isort --check --diff --profile black tests

echo "example code coding style check:"
pylint --recursive=y --rcfile=./example/.pylintrc --fail-under=10.0 example
black --check --diff example
isort --check --diff --profile black example
