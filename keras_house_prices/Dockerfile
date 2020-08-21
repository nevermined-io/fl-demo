FROM python:3.8-slim-buster
LABEL maintainer="Keyko <root@keyko.io>"

ARG VERSION

# lets cache tensorflow to reduce build time
RUN pip install tensorflow==2.2.0

COPY . /xain-participant
WORKDIR /xain-participant

RUN pip install .

ENTRYPOINT run-participant --help
