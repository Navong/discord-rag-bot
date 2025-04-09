# Variables
USERNAME = navong
IMAGE_NAME = discord-bot
TAG = latest
FULL_IMAGE = $(USERNAME)/$(IMAGE_NAME):$(TAG)

# Default target
.PHONY: all
all: build tag push

# Build the Docker image
.PHONY: build
build:
	docker build -t $(IMAGE_NAME):$(TAG) .

# Tag the image for Docker Hub
.PHONY: tag
tag:
	docker tag $(IMAGE_NAME):$(TAG) $(FULL_IMAGE)

# Push the image to Docker Hub
.PHONY: push
push:
	docker push $(FULL_IMAGE)

# Login to Docker Hub
.PHONY: login
login:
	docker login

# Run the container locally with docker-compose
.PHONY: run
run:
	docker-compose up

# Build and run locally
.PHONY: up
up: build
	docker-compose --env-file .env up -d

# Stop and remove containers
.PHONY: down
down:
	docker-compose down

# Clean up Docker images
.PHONY: clean
clean:
	docker rmi $(IMAGE_NAME):$(TAG) $(FULL_IMAGE) || true

# Full workflow: login, build, tag, push
.PHONY: deploy
deploy: login build tag push

# Help
.PHONY: help
help:
	@echo "Makefile commands:"
	@echo "  make build    - Build the Docker image"
	@echo "  make tag      - Tag the image for Docker Hub"
	@echo "  make push     - Push the image to Docker Hub"
	@echo "  make login    - Login to Docker Hub"
	@echo "  make run      - Run with docker-compose"
	@echo "  make up       - Build and run with docker-compose"
	@echo "  make down     - Stop and remove containers"
	@echo "  make clean    - Remove local Docker images"
	@echo "  make deploy   - Full workflow: login, build, tag, push"
	@echo "  make all      - Build, tag, and push"