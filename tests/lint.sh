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
	xargs -0 -L 1 ansible-lint \
	             -R -r tests/ansible_lint_rules/
###############################################################################
# SHELL LINT
###############################################################################
find . -name '*.sh' -not -name 'jswarm.sh' -print0 |
	xargs -0 -L 1 shellcheck \
	             -e 1090,1091,2093
# jswarm.sh specifically includes variables that need to be word-split based
# on user input. Error 2086 is the Shell warning to quote variables to avoid
# space splitting. However, two of the variables in this shell script are
# intended to be split when they get included as variables into the script.
find . -name 'jswarm.sh' -print0 |
	xargs -0 -L 1 shellcheck \
	             -e 1090,1091,2093,2086
###############################################################################
# PYTHON LINT
###############################################################################
find . -name '*.py' -print0 |
	xargs -0 -L 1 flake8
