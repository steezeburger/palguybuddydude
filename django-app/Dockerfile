FROM python:3.11-slim as base
ENV PYTHONUNBUFFERED 1

# install pipenv and compilation dependencies
# https://cryptography.io/en/latest/installation/
RUN apt-get update && apt-get install -y build-essential libssl-dev libffi-dev python3-dev cargo
RUN pip install --upgrade pip pipenv

# install python dependencies
RUN mkdir /code
WORKDIR /code
COPY Pipfile /code
COPY Pipfile.lock /code
RUN pipenv install --dev --deploy --system

# install application into container
COPY . /code

# run application
EXPOSE 8000

WORKDIR /code/app

# this CMD is overridden by the command in docker-compose.yml for local development
CMD /code/bin/wait-for-it.sh db:5432 -- python /code/app/manage.py runserver 0.0.0.0:8000
