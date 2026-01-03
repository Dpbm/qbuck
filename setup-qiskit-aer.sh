#!/usr/bin/env bash

set -e

SCRIPT_DIR="$(cd $(dirname ${BASH_SOURCE[0]}) && pwd)"

source $SCRIPT_DIR/utils.sh

MODIFIED_AER_PATH="$SCRIPT_DIR/modified-aer-venv"
if [ -d $MODIFIED_AER_PATH ]; then
    print_blue_line "Cleaning aer venv:  $MODIFIED_AER_PATH"
    rm -rf $MODIFIED_AER_PATH
fi


print_line "Set up new env for modified qiskit-AER"
python -m venv $MODIFIED_AER_PATH
source $MODIFIED_AER_PATH/bin/activate

print_line "build qiskit-AER"
cd $SCRIPT_DIR/qiskit-aer
rm -rf ./_skbuild
pip3 install .
cd ..

deactivate

print_green_line "Finished build"
