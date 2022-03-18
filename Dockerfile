FROM python:alpine

COPY dist/ /work/

RUN pip install --no-cache-dir --disable-pip-version-check pipdot --no-index --find-links file:///work/

ENTRYPOINT [ "pipdot" ]
CMD [ ]
