FROM python:alpine

COPY dist/ /opt/pyproject-dist/

RUN pip install --no-cache-dir --disable-pip-version-check pipdot --no-index --find-links file:///opt/pyproject-dist/

ENTRYPOINT [ "pipdot" ]
CMD [ ]
