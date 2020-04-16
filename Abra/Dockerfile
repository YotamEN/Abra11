FROM ubuntu:latest
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y --no-install-recommends ca-certificates make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
libffi-dev liblzma-dev git
RUN git clone https://github.com/pyenv/pyenv.git /pyenv
ENV PATH /pyenv:$PATH
RUN /pyenv/bin/pyenv install -v 3.8.0
RUN /pyenv/bin/pyenv global 3.8.0
RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY server.py server.py
CMD ["python", "server.py"]