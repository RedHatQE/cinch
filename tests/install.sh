#!/usr/bin/env sh
set -ve
pip install -U pip
pip install . ".[lint]" ".[test]"
