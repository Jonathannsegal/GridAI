# https://hub.docker.com/_/python
FROM python:3.10-slim
# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True
# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY src/requirements.txt ./

# Set up google credentials
COPY client_secret/speechtotext-331119-820cdd23000d.json /tmp/keys/
ENV GOOGLE_APPLICATION_CREDENTIALS "/tmp/keys/speechtotext-331119-820cdd23000d.json"

# Service must listen to $PORT environment variable.
ENV PORT 8080
# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Bundle app source
COPY src /app

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
