FROM python:3.8-slim

MAINTAINER Yotam Even-Nir <yotamevennir@mail.tau.ac.il>

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# ENV PYTHONPATH /app
# ENV FLASKAPP=server
ENV PYTHONPATH=/usr/local/bin

# WORKDIR /app

RUN pip3 install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY abra abra
COPY wait-for-it.sh wait-for-it.sh
RUN chmod +x wait-for-it.sh
CMD ['bash']