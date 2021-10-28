FROM node:15.9.0

WORKDIR /

COPY . /

RUN apt-get update && apt-get -y install nodejs

RUN npm install --legacy-peer-deps

EXPOSE 3000