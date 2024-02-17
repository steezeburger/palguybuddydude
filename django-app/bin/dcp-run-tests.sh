#! /bin/bash

# proxy to execute pytest in web container

docker-compose run --rm -w /code/app web pytest -m "not integration" --cov=. --verbose
