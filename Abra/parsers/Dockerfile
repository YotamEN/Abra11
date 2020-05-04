FROM ubuntu:latest

MAINTAINER Yotam Even-Nir <yotamevennir@mail.tau.ac.il>

# install system-wide deps for python and node
RUN apt-get -yqq update
RUN apt-get -yqq install python-pip python-dev curl gnupg

# copy our application code
ADD . .
WORKDIR /opt/parsers

# expose port
EXPOSE 5000

# start app
CMD [ "python", "-m abra.parsers run-parser 'pose' 'rabbitmq://127.0.0.1:5672/'" ]