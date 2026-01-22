#!/usr/bin/env bash

set -e
set -o pipefail

SCRIPT_DIR="$(cd $(dirname ${BASH_SOURCE[0]}) && pwd)"
source $SCRIPT_DIR/utils.sh

TARGET_ASSETS_FOLDER="$SCRIPT_DIR/assets"

for dot_file in $SCRIPT_DIR/*.dot; do
	OUTPUT_FILE_NAME=$(sed 's|\.dot|.png|g' <<< $dot_file | sed 's|^.*\/||g' )
	OUTPUT_FILE_PATH="$TARGET_ASSETS_FOLDER/$OUTPUT_FILE_NAME"
	print_blue_line "running $dot_file and saving output in $OUTPUT_FILE_PATH..."
	dot -Tpng $dot_file >> "$OUTPUT_FILE_PATH"
done
