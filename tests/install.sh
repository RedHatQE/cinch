#!/usr/bin/env sh
set -ve
pip install -U pip
pip install . .[lint]
for image in greghellings/centos_base:7 \
             greghellings/centos_base:6; do
	docker pull "${image}"
done
