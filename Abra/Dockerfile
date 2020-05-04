FROM ubuntu:latest

MAINTAINER Yotam Even-Nir <yotamevennir@mail.tau.ac.il>

# install system-wide deps for python and node
RUN apt-get -yqq update
RUN apt-get -yqq install python-pip python-dev

# install app deps
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

# copy our application code
ADD . /opt/app
WORKDIR /opt/app

# expose port
EXPOSE 6500

# start app
CMD [ "python", "./server.py" ]
