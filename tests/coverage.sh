#!/bin/bash -e

py.test --cov=cinch/bin --cov-config .coveragerc --cov-report term \
    --cov-report xml --cov-report html tests

codecov
