FROM python:3.8


RUN apt-get update -y && \
    apt-get install -y python-pip python-dev
COPY . /app
WORKDIR /app
RUN pip install  -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python" ]
CMD ["api.py"]
