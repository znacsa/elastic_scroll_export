#!/bin/bash
export SCRIPT_DIR=`dirname "$(readlink -f "$0")"`

source ${SCRIPT_DIR}/.python.conf

test -d ${SCRIPT_DIR}/python_v${PYTHON_VERSION} || python${PYTHON_VERSION} -m venv ${SCRIPT_DIR}/python_v${PYTHON_VERSION}
source ${SCRIPT_DIR}/python_v${PYTHON_VERSION}/bin/activate

pip install --upgrade pip
pip install --requirement ${SCRIPT_DIR}/requirements.pip
