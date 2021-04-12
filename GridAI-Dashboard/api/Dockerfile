FROM python:3.8


RUN apt-get update -y && \
    apt-get install -y python-pip python-dev
COPY . /app
WORKDIR /app
RUN python3 -m pip install  -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python3" ]
CMD ["api.py"]
