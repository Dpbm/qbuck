#!/usr/bin/env bash

source ./colors.sh

print_line(){
    echo $1
}

print_blue_line(){
    echo -e "$BLUE$1$RESET"
}

print_green_line(){
    echo -e "$GREEN$1$RESET"
}