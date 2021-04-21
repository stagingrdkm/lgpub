FROM python:3.6
FROM ubuntu:18.04
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y \
  python3.6-dev \
  python3-pip \
  vim \
  && rm -rf /var/lib/apt/lists/*

COPY required-packages.txt /
RUN pip3 install -r /required-packages.txt
COPY test_framework/ /test_framework
ENV PYTHONPATH "${PYTHONPATH}:/test_framework"
