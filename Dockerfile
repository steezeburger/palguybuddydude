# Start from the latest golang base image
FROM golang:latest

# Set the Current Working Directory inside the container
WORKDIR /app

# Copy go.mod and go.sum if they exist
COPY go.mod go.sum ./

# Download all dependencies if they exist
# If you're using Go modules, this will ensure they are cached.
RUN if [ -f go.mod ]; then go mod download; fi

# Copy the source from the current directory to the Working Directory inside the container
COPY . .

# Install CompileDaemon for hot reloading
RUN go build main.go

# Command to run the executable
ENTRYPOINT ["./main"]
