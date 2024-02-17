#! /bin/bash

data_to_load="dev_data.json"

function usage() {
  echo "Use this script to recreate the Docker volume and container for maya_postgres."
  echo "It also runs migrations and loads initial data according to \`--data\`,"
  echo "or \`dev_data.json\` by default if no \`--data\` parameter specified."
  echo ""
  echo "Usage:"
  echo "./utils/reload-docker-db.sh --help"
  echo "./utils/reload-docker-db.sh"
  echo "./utils/reload-docker-db.sh --data=demo_data.json"
  echo ""
}

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
    echo "You are trying to reload the database at ${DB_HOST}!"
    checkconfidence
  else
    echo "Reloading database at $DB_HOST"
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

function recreate() {
  # make sure db container is stopped
  docker-compose stop db

  # deletes postgres docker container
  docker-compose rm -f db

  # deletes postgres volume
  docker volume rm pgbd_postgres

  # recreates named volume
  docker volume create --name=pgbd_postgres

  # bring container back up and sleep for 5 seconds to ensure db is up
  docker-compose up -d db
  sleep 5
}

function migrate() {
  # run migrations
  docker-compose run --rm -w /code/app web /code/app/manage.py migrate
}

function loaddata() {
  # load data from fixture
  docker-compose run --rm -w /code/app web /code/app/manage.py loaddata $data_to_load
}

while [ "$1" != "" ]; do
  PARAM=$(echo $1 | awk -F= '{print $1}')
  VALUE=$(echo $1 | awk -F= '{print $2}')
  case $PARAM in
  -h | --help)
    usage
    exit
    ;;
  --data)
    data_to_load=$VALUE
    ;;
  *)
    echo "ERROR: unknown parameter \"$PARAM\""
    usage
    exit 1
    ;;
  esac
  shift
done


checkenv
echo "starting script ..."
echo "Reloading $DB_HOST w/ $data_to_load ..."
echo ""

echo "recreating volume and container ..."
recreate

echo "running migrations ..."
migrate

echo "loading data from ${data_to_load} ..."
loaddata
