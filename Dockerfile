FROM python:3.8-slim-buster
LABEL maintainer="Keyko <root@keyko.io>"

ARG VERSION

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

COPY . /xain-participant
WORKDIR /xain-participant

RUN pip install .

ENTRYPOINT run-participant --help
