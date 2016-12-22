#!/bin/bash

set -x

TOP=$(readlink -f "$(dirname "${0}")/../../")

function venv {
    /bin/bash "${TOP}/bin/ensure_virtualenv.sh" || exit 1
}

function playbook {
    source "${TOP}/.venv/bin/activate"
    directory="${1}"
    shift
    export ANSIBLE_CONFIG="${TOP}/vagrant/ansible.cfg"
    cinch "${TOP}/vagrant/${directory}/hosts" \
        -e "vagrant_dir=${TOP}/vagrant/${directory}" \
        "$@" || exit 1
    deactivate
}

function vagrant_cycle {
    cd "${TOP}/vagrant/${1}/" || exit 1
    vagrant destroy -f || exit 1
    vagrant up || exit 1
}
