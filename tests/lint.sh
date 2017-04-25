#!/usr/bin/env sh
set -ve

###############################################################################
# ANSIBLE LINT
###############################################################################
find cinch -maxdepth 1 -name '*.yml' \
	-execdir ansible-playbook \
	             --syntax-check \
	             -i ../inventory/sample/hosts \
	             '{}' \;
find cinch -maxdepth 1 -name '*.yml' \
	-execdir ansible-lint \
	             '{}' \;
###############################################################################
# SHELL LINT
###############################################################################
find . -name '*.sh' -not -name 'jswarm.sh' \
	-execdir shellcheck \
	             -e 1090,1091,2093 \
	             '{}' \;
find . -name 'jswarm.sh' \
	-execdir shellcheck \
	             -e 1090,1091,2093,2086 \
	             '{}' \;
###############################################################################
# PYTHON LINT
###############################################################################
find . -name '*.py' \
	-execdir flake8 \
	             '{}' \;
