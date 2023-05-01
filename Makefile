SHELL := /bin/bash
PWD := $(shell pwd)

GIT_REMOTE = github.com/7574-sistemas-distribuidos/docker-compose-init

default: build

all:

client-image:
	docker build -f ./client/Dockerfile -t "client:latest" .
.PHONY: client-image

server-image:
	docker build -f ./receiver/Dockerfile -t "receiver:latest" .

	docker build -f ./handlers/stations_handler/Dockerfile -t "stations_handler:latest" .
	docker build -f ./handlers/eof_manager/Dockerfile -t "em_handlers:latest" .

	docker build -f ./filters/filter_trips/Dockerfile -t "filter_trips:latest" .
	docker build -f ./filters/filter_trips_stations/Dockerfile -t "filter_trips_stations:latest" .
	docker build -f ./filters/eof_manager/Dockerfile -t "em_filters:latest" .

	docker build -f ./query2/applier/Dockerfile -t "applier_2:latest" .
	docker build -f ./query2/groupby/Dockerfile -t "groupby_2:latest" .
	
	docker build -f ./query_state_verifier/Dockerfile -t "query_state_verifier:latest" .

	docker build -f ./eof_manager/groupby/Dockerfile -t "em_groupby:latest" .
	docker build -f ./eof_manager/applier/Dockerfile -t "em_applier:latest" .
	docker build -f ./eof_manager/query_state_verifier/Dockerfile -t "em_query_state_verifier:latest" .
.PHONY: server-image

server-up: server-image
	docker compose -f docker-compose-dev.yaml up -d --build
.PHONY: server-up

client-run: client-image
	docker compose -f docker-compose-client.yaml up -d --build
	docker compose -f docker-compose-client.yaml logs -f
.PHONY: client-run

server-down:
	docker compose -f docker-compose-dev.yaml stop -t 1
	docker compose -f docker-compose-dev.yaml down
.PHONY: server-down

client-down:
	docker compose -f docker-compose-client.yaml stop -t 1
	docker compose -f docker-compose-client.yaml down
.PHONY: client-down

server-logs:
	docker compose -f docker-compose-dev.yaml logs -f
.PHONY: server-logs

server-run: server-image
	docker compose -f docker-compose-dev.yaml up -d --build
	docker compose -f docker-compose-dev.yaml logs -f
.PHONY: server-run