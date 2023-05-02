SHELL := /bin/bash
PWD := $(shell pwd)

GIT_REMOTE = github.com/7574-sistemas-distribuidos/docker-compose-init

default: build

all:

server-image:
	docker build -f ./client/Dockerfile -t "client:latest" .

	docker build -f ./receiver/Dockerfile -t "receiver:latest" .

	docker build -f ./joiners/stations_handler/Dockerfile -t "stations_handler:latest" .
	docker build -f ./joiners/weather_handler/Dockerfile -t "weather_handler:latest" .

	docker build -f ./filters/filter_trips/Dockerfile -t "filter_trips:latest" .
	docker build -f ./filters/filter_trips_stations/Dockerfile -t "filter_trips_stations:latest" .
	docker build -f ./filters/filter_trips_weather/Dockerfile -t "filter_trips_weather:latest" .

	docker build -f ./queries/query1/applier/Dockerfile -t "applier_1:latest" .
	docker build -f ./queries/query1/groupby/Dockerfile -t "groupby_1:latest" .
	docker build -f ./queries/query2/applier/Dockerfile -t "applier_2:latest" .
	docker build -f ./queries/query2/groupby/Dockerfile -t "groupby_2:latest" .
	docker build -f ./queries/query3/applier/Dockerfile -t "applier_3:latest" .
	docker build -f ./queries/query3/groupby/Dockerfile -t "groupby_3:latest" .
	
	docker build -f ./query_state_verifier/Dockerfile -t "query_state_verifier:latest" .

	docker build -f ./eof_manager/joiner/Dockerfile -t "em_joiners:latest" .
	docker build -f ./eof_manager/filter/Dockerfile -t "em_filters:latest" .
	docker build -f ./eof_manager/groupby/Dockerfile -t "em_groupby:latest" .
	docker build -f ./eof_manager/applier/Dockerfile -t "em_applier:latest" .
.PHONY: server-image

server-up: server-image
	docker compose -f docker-compose-dev.yaml up -d --build
.PHONY: server-up

server-down:
	docker compose -f docker-compose-dev.yaml stop -t 1
	docker compose -f docker-compose-dev.yaml down
.PHONY: server-down

server-logs:
	docker compose -f docker-compose-dev.yaml logs -f
.PHONY: server-logs

server-run: server-image
	docker compose -f docker-compose-dev.yaml up -d --build
	docker compose -f docker-compose-dev.yaml logs -f
.PHONY: server-run