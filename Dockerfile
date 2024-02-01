# Start from the latest golang base image
FROM golang:latest

WORKDIR /app

COPY go.mod go.sum ./

RUN go mod download

COPY . .

RUN go build main.go

ENTRYPOINT ["./main"]
