# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.8

# Allow statements and log messages to immediately appear in the Cloud Run logs
ENV PYTHONUNBUFFERED True

# Install git dependency
RUN apt-get install -y git

# Copy application dependency manifests to the container image.
# Copying this separately prevents re-running pip install on every code change.
COPY requirements.txt ./

# Install production dependencies.
RUN pip install -r requirements.txt

# Copy local code to the container image.
ENV APP_HOME /app
ENV PRODUCTION=1
WORKDIR $APP_HOME
COPY . ./

# Execute Scraper
CMD ["scrapy", "crawl", "family"]
