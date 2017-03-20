#!/usr/bin/env sh
set -ve
pip install -U pip
pip install . .[lint]
docker pull greghellings/centos_base:{7,6}
