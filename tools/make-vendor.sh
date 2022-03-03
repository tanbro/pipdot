#!/usr/bin/env sh

( \
VENDOR_DIR=src/pipdot/_vendor && \
CIBUILDWHEEL=0 && \
(cd ${VENDOR_DIR} && while read -r entry;do rm -rf ${entry}; done < .gitignore) && \
python3 -m pip install --upgrade --no-compile -t ${VENDOR_DIR} -r requires/vendor.txt && \
echo "" > ${VENDOR_DIR}/__init__.py && \
rm -rf ${VENDOR_DIR}/*.dist-info/ && \
rm -rf ${VENDOR_DIR}/markupsafe/_speedups.* \
)
