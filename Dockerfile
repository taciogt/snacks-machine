FROM python:3.8.6-alpine3.11
ENV PYTHONUNBUFFERED 1
ARG DEBIAN_FRONTEND=noninteractive

RUN mkdir /app
WORKDIR /app

RUN pip install pipenv
COPY Pipfile /app
COPY Pipfile.lock /app
RUN pipenv install --system --deploy --verbose --ignore-pipfile

#COPY ./backend /app/
#COPY ./core /app/