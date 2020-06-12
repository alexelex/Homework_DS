FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR authorization
ADD authorization .
ADD genrpc genrpc
RUN pip install -r requirements.txt
