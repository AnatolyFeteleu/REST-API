FROM python:3.6
ENV PYTHONBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN pip install -r requirements.txt
RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "nano"]
