#!/bin/bash
export SCRIPT_DIR=`dirname "$(readlink -f "$0")"`

source ${SCRIPT_DIR}/.python.conf
source ${SCRIPT_DIR}/python_v${PYTHON_VERSION}/bin/activate

python ${SCRIPT_DIR}/elastic_scroll_export.py $@
