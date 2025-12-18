#!/usr/bin/env bash

set -e

source ./utils.sh
source ./setup-qiskit-aer.sh

print_blue_line "Setup qiskit-aer modified version...."
setup_aer

print_blue_line "Run classical version..."
uv run python classical.py

print_blue_line "Run quantum default version..."
uv run python quantum_default_version.py

print_blue_line "Run quantum modified version..."
uv run python quantum_modified_version.py

print_blue_line "Run noisy version..."
CERTS_PATH=/etc/ssl/certs/ca-certificates.crt #change it depending on your system
REQUESTS_CA_BUNDLE=$CERTS_PATH uv run --native-tls python quantum_noisy.py

print_blue_line "Running the notebook..."
uv run jupyter nbconvert --execute analysis.ipynb --inplace

print_green_line "finished!"
