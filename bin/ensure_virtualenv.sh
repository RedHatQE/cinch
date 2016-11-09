#!/bin/bash

TOP=$(dirname $(readlink -f $(dirname $0)))

# Create the basic virtualenv into which the software will be installed
if [ ! -d "${TOP}/.venv" ]; then
    virtualenv "${TOP}/.venv"
fi

# Update the virtualenv to include all the necessary utilities
source "${TOP}/.venv/bin/activate"
pip install pip==9.0.1
pip install -e "${TOP}"
