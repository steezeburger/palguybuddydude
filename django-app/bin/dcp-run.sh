#! /bin/bash

# proxy to run shell commands in web container.
# `run --rm` starts and runs container, then removes itself to cleanup

docker-compose run --rm web "$@"
