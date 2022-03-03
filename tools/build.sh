#!/usr/bin/env bash

sh tools/make-vendor.sh && \
python -m build
