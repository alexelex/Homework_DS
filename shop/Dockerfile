FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR shop
ADD shop .
ADD genrpc genrpc
RUN pip install -r requirements.txt
