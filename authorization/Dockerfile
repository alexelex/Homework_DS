FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /auth_code
WORKDIR /auth_code
COPY requirements.txt /auth_code/
RUN pip install -r requirements.txt
COPY . /auth_code/
