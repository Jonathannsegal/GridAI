FROM node:15.9.0

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev


ADD . /app

WORKDIR /app

RUN ls

RUN cat app.py

RUN pip install -r requirements.txt