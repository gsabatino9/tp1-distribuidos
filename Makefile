SHELL := /bin/bash
PWD := $(shell pwd)

GIT_REMOTE = github.com/7574-sistemas-distribuidos/docker-compose-init

default: build

all:

client-image:
	docker build -f ./client/Dockerfile -t "client:latest" .
.PHONY: client-image

server-image:
	docker build -f ./server/receiver/Dockerfile -t "receiver:latest" .
	docker build -f ./server/joiners/joiner_stations/Dockerfile -t "joiner_stations:latest" .
	docker build -f ./server/joiners/joiner_weather/Dockerfile -t "joiner_weather:latest" .
	
	docker build -f ./server/filters/filter_pretoc/Dockerfile -t "filter_pretoc:latest" .
	docker build -f ./server/filters/filter_year/Dockerfile -t "filter_year:latest" .
	docker build -f ./server/filters/filter_distance/Dockerfile -t "filter_distance:latest" .
	
	docker build -f ./server/groupby/query1/Dockerfile -t "groupby_query1:latest" .
	docker build -f ./server/groupby/query2/Dockerfile -t "groupby_query2:latest" .
	docker build -f ./server/groupby/query3/Dockerfile -t "groupby_query3:latest" .
	
	docker build -f ./server/applier/query1/Dockerfile -t "applier_query1:latest" .
	docker build -f ./server/applier/query2/Dockerfile -t "applier_query2:latest" .
	docker build -f ./server/applier/query3/Dockerfile -t "applier_query3:latest" .
	
	docker build -f ./server/eof_manager/joiners/Dockerfile -t "eof_manager_joiners:latest" .
	docker build -f ./server/eof_manager/filters/Dockerfile -t "eof_manager_filters:latest" .
	docker build -f ./server/eof_manager/groupby/Dockerfile -t "eof_manager_groupby:latest" .
	docker build -f ./server/eof_manager/applier/Dockerfile -t "eof_manager_applier:latest" .
.PHONY: server-image

server-up: server-image
	docker compose -f docker-compose-server.yaml up -d --build
.PHONY: server-up

server-down:
	docker compose -f docker-compose-server.yaml stop -t 1
	docker compose -f docker-compose-server.yaml down
.PHONY: server-down

server-logs:
	docker compose -f docker-compose-server.yaml logs -f
.PHONY: server-logs

server-run: server-image
	docker compose -f docker-compose-server.yaml up -d --build
	docker compose -f docker-compose-server.yaml logs -f
.PHONY: server-run

client-run: client-image
	docker compose -f docker-compose-client.yaml up -d --build
	docker compose -f docker-compose-client.yaml logs -f
.PHONY: client-run

client-down:
	docker compose -f docker-compose-client.yaml stop -t 1
	docker compose -f docker-compose-client.yaml down
.PHONY: client-down