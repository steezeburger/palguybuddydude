#! /bin/bash

# prints a secret key to be used for django settings
docker-compose run --rm -w /code/app web python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
