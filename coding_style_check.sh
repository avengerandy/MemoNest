#!/bin/bash

echo "main code coding style check:"
pylint --recursive=y --rcfile=./src/.pylintrc src
black --check --diff src
isort --diff --profile black src

echo "test code coding style check:"
pylint --recursive=y --rcfile=./tests/.pylintrc tests
black --check --diff tests
isort --diff --profile black tests

echo "example code coding style check:"
pylint --recursive=y --rcfile=./example/.pylintrc example
black --check --diff example
isort --diff --profile black example
