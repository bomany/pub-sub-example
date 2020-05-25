FROM python:3.7-slim-buster
ENV PYTHONUNBUFFERED 1
ENV SHELL /bin/bash
ENV PYTHONPATH "${PYTHONPATH}:/project"

RUN mkdir project
WORKDIR /project

RUN apt-get update && apt-get install -y \
    gettext \
    git \
    gcc \
&& apt-get clean

ADD ./requirements.txt /project/requirements.txt
RUN pip config --global set install.src '/usr/local/lib/python3.7/src'
RUN pip install -r requirements.txt

ADD . /project
