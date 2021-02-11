FROM python:3.8

RUN mkdir /opt/src

WORKDIR /opt/src
ADD . /opt/src/

RUN pip install --no-cache-dir -r requirements.txt