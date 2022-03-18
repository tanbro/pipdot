#!/usr/bin/env bash

set -e

( 
    VENDOR_DIR=src/pipdot/_vendor 
    CIBUILDWHEEL=0
    pip install --upgrade --no-compile -t ${VENDOR_DIR} -r requires/vendor.txt
    pip freeze  --path ${VENDOR_DIR} | tee ${VENDOR_DIR}/freeze.txt
    rm -fr ${VENDOR_DIR}/*.dist-info/
    rm -fr ${VENDOR_DIR}/markupsafe/_speedups.*
)
