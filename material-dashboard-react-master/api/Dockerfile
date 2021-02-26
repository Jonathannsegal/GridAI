FROM node:15.9.0

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COP