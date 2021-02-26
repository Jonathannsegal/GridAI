FROM node:15.9.0

WORKDIR /

ADD . /

RUN apt-get update; apt-get -y install nodejs

RUN npm install

EXPOSE 3000