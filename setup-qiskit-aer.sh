#!/usr/bin/env bash

setup_aer(){
    source ./utils.sh

    local MODIFIED_AER_PATH="./modified-aer-venv"
    print_blue_line "Cleaning aer venv:  $MODIFIED_AER_PATH"
    rm -rf $MODIFIED_AER_PATH

    set -e

    print_line "Set up new env for modified qiskit-AER"
    python -m venv $MODIFIED_AER_PATH
    source $MODIFIED_AER_PATH/bin/activate

    print_line "build qiskit-AER"
    cd ./qiskit-aer
    rm -rf ./_skbuild
    pip install .
    cd ..

    deactivate

    print_green_line "Finished build"
}
