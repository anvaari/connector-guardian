ARG PYTHON_VERSION=3.9

FROM python:${PYTHON_VERSION}

LABEL maintainer="anvaari@proton.me"

RUN pip install -U pip &&  \
    pip install -r requirements.txt

COPY . /connector-guardian