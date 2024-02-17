#! /bin/bash

# proxy to execute shell commands in running web container

docker-compose exec web "$@"
