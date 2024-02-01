default:
  @just --list

set dotenv-load

# run go binary
run:
  go run main.go

fmt:
  go fmt ./...

docker-build:
  docker buildx build -t palguybuddydude:local .
