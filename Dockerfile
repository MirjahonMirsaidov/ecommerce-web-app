FROM python:3.9-alpine
MAINTAINER Mirsaidov Mirjahon

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /container
WORKDIR /container
COPY ./container /container

RUN adduser -D user
USER user