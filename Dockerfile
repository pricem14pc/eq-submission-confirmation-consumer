FROM python:3.8-slim-buster

RUN apt update && apt install -y curl unzip libsnappy-dev build-essential jq

WORKDIR /app
COPY . /app

ENV PYTHONPATH /app

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pip install pipenv==2018.11.26

RUN pipenv install --deploy --system

CMD [ "python", "./app/pub_sub_consumer.py" ]