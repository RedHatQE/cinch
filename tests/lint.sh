#!/usr/bin/env sh
set -ve

ansible-playbook --syntax-check "cinch/site.yml"
ansible-playbook --syntax-check "cinch/teardown.yml"

find . -name '*.sh' -not -name 'jswarm.sh' -print0 | xargs -0 shellcheck -e 1090,1091,2093
find . -name 'jswarm.sh' -print0 | xargs -0 shellcheck -e 1090,1091,2093,2086

SOURCES=$(find . -name '*.py')
for src in ${SOURCES}; do
    flake8 "${src}"
done
