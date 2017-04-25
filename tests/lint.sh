#!/usr/bin/env sh
set -ve

###############################################################################
# ANSIBLE LINT
###############################################################################
find cinch -maxdepth 1 -name '*.yml' -print0 |
	xargs -0 -L 1 ansible-playbook \
	             --syntax-check \
	             -i inventory/sample/hosts
find cinch -maxdepth 1 -name '*.yml' -print0 |
	xargs -0 -L 1 ansible-lint
###############################################################################
# SHELL LINT
###############################################################################
find . -name '*.sh' -not -name 'jswarm.sh' -print0 |
	xargs -0 -L 1 shellcheck \
	             -e 1090,1091,2093
find . -name 'jswarm.sh' -print0 |
	xargs -0 -L 1 shellcheck \
	             -e 1090,1091,2093,2086
###############################################################################
# PYTHON LINT
###############################################################################
find . -name '*.py' -print0 |
	xargs -0 -L 1 flake8
