#!/usr/bin/env bash

( 
    VENDOR_DIR=src/pipdot/_vendor 
    CIBUILDWHEEL=0
    python3 -m pip install --upgrade --no-compile -t ${VENDOR_DIR} -r requires/vendor.txt
    rm -rf ${VENDOR_DIR}/*.dist-info/ 
    rm -rf ${VENDOR_DIR}/markupsafe/_speedups.* 
)
