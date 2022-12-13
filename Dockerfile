FROM python:alpine

RUN --mount=type=bind,source=dist,target=/root/dist/ \
    pip install --disable-pip-version-check pipdot --no-index --find-links file:///root/dist/ && \
    rm -rf /root/dist/

ENTRYPOINT [ "pipdot" ]
CMD [ ]
