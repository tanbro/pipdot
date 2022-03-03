#!/usr/bin/env sh

sh tools/make-vendor.sh && \
python -m build
