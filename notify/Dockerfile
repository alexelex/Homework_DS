FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /notify_code
WORKDIR /notify_code
COPY requirements.txt /notify_code/
RUN pip install -r requirements.txt
COPY notify /notify_code/
