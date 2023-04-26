SHELL := /bin/bash
PWD := $(shell pwd)

default: build

all:

client-image:
	docker build -f ./client/client.dockerfile -t "client:latest" .
.PHONY: client-image

server-image:
	docker build -f ./receiver/receiver.dockerfile -t "receiver:latest" .
	docker build -f ./stations_handler/stations_handler.dockerfile -t "stations_handler:latest" .
.PHONY: server-image

server-up: server-image
	docker-compose -f docker-compose-dev.yaml up -d --build
.PHONY: server-up

client-up: client-image
	docker-compose -f docker-compose-client.yaml up -d --build
.PHONY: client-up

server-down:
	docker-compose -f docker-compose-dev.yaml stop -t 1
	docker-compose -f docker-compose-dev.yaml down
.PHONY: server-down

client-down:
	docker-compose -f docker-compose-client.yaml stop -t 1
	docker-compose -f docker-compose-client.yaml down
.PHONY: client-down

server-logs:
	docker-compose -f docker-compose-dev.yaml logs -f
.PHONY: server-logs

server-run: server-image
	docker-compose -f docker-compose-dev.yaml up -d --build
	docker-compose -f docker-compose-dev.yaml logs -f
.PHONY: server-run