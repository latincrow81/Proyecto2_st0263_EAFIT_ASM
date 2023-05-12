FROM python:3.9.7-alpine

WORKDIR /usr/src/app

RUN apk add build-base
RUN apk update && apk add gcc python3-dev musl-dev curl py3-setuptools

ADD api_gateway .
RUN pip install -r requirements.txt

RUN chmod +x docker-entrypoint.sh
COPY api_gateway/docker-entrypoint.sh /

CMD ["#!/bin/sh", "docker-entrypoint.sh"]