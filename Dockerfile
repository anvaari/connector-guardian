ARG PYTHON_VERSION=3.9

FROM python:${PYTHON_VERSION}-alpine

LABEL maintainer="anvaari@proton.me"

COPY . /connector-guardian

RUN pip install -U pip &&  \
    pip install -r /connector-guardian/requirements.txt

