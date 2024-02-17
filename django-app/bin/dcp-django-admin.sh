#! /bin/bash

# proxy to execute `manage.py` (django-admin) commands in web container

function checkenv() {
  ##############################################################
  # check user's confidence if we are not using local database #
  ##############################################################

  # get db host envar from docker container
  DB_HOST_ENVAR=$(docker-compose run --rm -w /code/app web env | grep POSTGRES_HOST)
  DB_HOST=$(cut -d "=" -f2 <<< "$DB_HOST_ENVAR")
  # bashism to trim newline
  DB_HOST=${DB_HOST//[$'\t\r\n']}
  if [ "$DB_HOST" != 'db' ] && [ "$DB_HOST" != '0.0.0.0' ] && [ "$DB_HOST" != 'localhost' ]
  then
    echo "You are running this command against the database at ${DB_HOST}!"
    checkconfidence
  else
    echo "Running command against database at $DB_HOST..."
  fi
}

function checkconfidence() {
  read -r -p "Are you sure you want to continue? [y/N] " response
  if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
  then
    return
  else
    exit
  fi
}

checkenv
docker-compose run --rm -w /code/app web /code/app/manage.py "$@"
