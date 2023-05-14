import sys
from init_config import *

NAME_STATIONS_QUEUE = "joiner_stations_q"
NAME_WEATHER_QUEUE = "joiner_weather_q"
NAME_TRIPS_QUEUES = ["join_trip_weather_q", "join_trip_stations_q"]
NAME_EM_JOINERS_QUEUE = "eof_manager_joiners_q"
NAME_FILTER_STATIONS_QUEUE = "filter_joined_stations_q"
NAME_FILTER_WEATHER_QUEUE = "filter_joined_weather_q"


def main():
    num_filters_pretoc = int(sys.argv[1])
    num_filters_year = int(sys.argv[2])
    num_filters_distance = int(sys.argv[3])
    num_appliers_query1 = int(sys.argv[4])
    num_appliers_query2 = int(sys.argv[5])
    num_appliers_query3 = int(sys.argv[6])

    receiver = RECEIVER.format(
        NAME_STATIONS_QUEUE,
        NAME_WEATHER_QUEUE,
        NAME_TRIPS_QUEUES,
        NAME_EM_JOINERS_QUEUE,
    )
    joiner_stations = JOINER_STATIONS.format(
        NAME_STATIONS_QUEUE,
        NAME_TRIPS_QUEUES[1],
        NAME_EM_JOINERS_QUEUE,
        NAME_FILTER_STATIONS_QUEUE,
    )
    joiner_weather = JOINER_WEATHER.format(
        NAME_WEATHER_QUEUE,
        NAME_TRIPS_QUEUES[0],
        NAME_EM_JOINERS_QUEUE,
        NAME_FILTER_WEATHER_QUEUE,
    )

    filters_pretoc = ""
    for i in range(1, num_filters_pretoc + 1):
        filters_pretoc += FILTER_PRETOC.format(i, i)

    filters_year = ""
    for i in range(1, num_filters_year + 1):
        filters_year += FILTER_YEAR.format(i, i)

    filters_distance = ""
    for i in range(1, num_filters_distance + 1):
        filters_year += FILTER_DISTANCE.format(i, i)

    em_filters = EM_FILTERS.format(
        [num_filters_pretoc, num_filters_year, num_filters_distance]
    )

    appliers_query1 = ""
    for i in range(1, num_appliers_query1 + 1):
        appliers_query1 += APPLIER_QUERY1.format(i, i)

    appliers_query2 = ""
    for i in range(1, num_appliers_query2 + 1):
        appliers_query2 += APPLIER_QUERY2.format(i, i)

    appliers_query3 = ""
    for i in range(1, num_appliers_query3 + 1):
        appliers_query3 += APPLIER_QUERY3.format(i, i)

    em_appliers = EM_APPLIERS.format(
        [num_appliers_query1, num_appliers_query2, num_appliers_query3]
    )

    compose = (
        INIT_DOCKER.format()
        .replace("<RECEIVER>", receiver)
        .replace("<JOINER_STATIONS>", joiner_stations)
        .replace("<JOINER_WEATHER>", joiner_weather)
        .replace("<FILTER_PRETOC>", filters_pretoc)
        .replace("<FILTER_YEAR>", filters_year)
        .replace("<FILTER_DISTANCE>", filters_distance)
        .replace("<EM_FILTERS>", em_filters)
        .replace("<EM_GROUPBY>", EM_GROUPBY)
        .replace("<GROUPBY_QUERY1>", GROUPBY_QUERY1)
        .replace("<GROUPBY_QUERY2>", GROUPBY_QUERY2)
        .replace("<GROUPBY_QUERY3>", GROUPBY_QUERY3)
        .replace("<APPLIER_QUERY1>", appliers_query1)
        .replace("<APPLIER_QUERY2>", appliers_query2)
        .replace("<APPLIER_QUERY3>", appliers_query3)
        .replace("<EM_APPLIERS>", em_appliers)
        .replace("<EM_RESULTS>", EM_RESULTS)
        .replace("<RESULTS_VERIFIER>", RESULTS_VERIFIER)
    )

    with open("docker-compose-server.yaml", "w") as compose_file:
        compose_file.write(compose)


if __name__ == "__main__":
    main()
