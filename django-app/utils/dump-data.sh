#! /bin/bash

# script that dumps data from postgres

docker-compose run --rm -w /code/app web /code/app/manage.py dumpdata \
  --natural-primary \
  --natural-foreign \
  --exclude=admin.logentry \
  --exclude=sessions.session \
  --indent 4
