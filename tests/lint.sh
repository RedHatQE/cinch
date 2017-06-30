#!/usr/bin/env sh
set -ve

cinch="$(readlink -f "$(dirname "${0}")/../")"
###############################################################################
# ANSIBLE LINT
###############################################################################
find "${cinch}" \( \( -path "${cinch}/build" -o -path "${cinch}/.git" \) \
	-prune -o -name '*.yml' \) \
	-type f -print0 |
	xargs -0 -L 1 yamllint \
	                  -c "${cinch}/tests/yamllint.yml"
yamllint -c "${cinch}/tests/yamllint.yml" "${cinch}"/cinch/group_vars/*
find "${cinch}/cinch" -maxdepth 2 -name '*.yml' -print0 |
	xargs -0 -L 1 ansible-playbook \
	             --syntax-check \
	             -i "${cinch}/inventory/sample/hosts"
find "${cinch}/cinch" -maxdepth 2 -name '*.yml' -print0 |
	xargs -0 -L 1 ansible-lint \
	             -R -r "${cinch}/tests/ansible_lint_rules/"
###############################################################################
# SHELL LINT
###############################################################################
find "${cinch}" -name '*.sh' -not -name 'jswarm.sh' -print0 |
	xargs -0 -L 1 shellcheck \
	             -e 1090,1091,2093
# jswarm.sh specifically includes variables that need to be word-split based
# on user input. Error 2086 is the Shell warning to quote variables to avoid
# space splitting. However, two of the variables in this shell script are
# intended to be split when they get included as variables into the script.
find "${cinch}" -name 'jswarm.sh' -print0 |
	xargs -0 -L 1 shellcheck \
	             -e 1090,1091,2093,2086
###############################################################################
# PYTHON LINT
###############################################################################
# jenkins_script.py was vendored from upstream Ansible.
# It can be removed once linchpin depends on ansible>=2.3
# https://docs.ansible.com/ansible/jenkins_script_module.html
find "${cinch}" -name '*.py' -not -name 'jenkins_script.py' -print0 |
	xargs -0 -L 1 flake8
