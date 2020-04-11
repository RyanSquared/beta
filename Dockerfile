FROM tiangolo/uwsgi-nginx-flask:python3.7

# Git-versioned dependencies
RUN pip3 install git+https://github.com/RyanSquared/gigaspoon
RUN pip3 install git+https://github.com/mediapanel/util

# Custom dependencies
RUN pip3 install cryptography

COPY . /app
WORKDIR /app

# Install for MySQL testing
RUN pip3 install .[mysql]
