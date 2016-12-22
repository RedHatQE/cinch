#!/usr/bin/env sh
set -ve

ansible-playbook --syntax-check "cinch/site.yml"

find . -name '*.sh' -print0 | xargs -0 shellcheck -e 1090,1091

SOURCES=$(find . -name '*.py')
for src in ${SOURCES}; do
    flake8 "${src}"
done
