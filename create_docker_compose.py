import sys, json
from init_config import *


def main():
    with open("config.json") as f:
        json_config = json.load(f)

    queues = json_config["config"]["queues"]
    em_queues = json_config["config"]["eof_manager_queues"]
    amount_nodes = json_config["config"]["amount_nodes"]

    receiver = RECEIVER.format(
        queues["joiners"]["stations"],
        queues["joiners"]["weather"],
        [
            queues["joiners"]["join_trip_stations"],
            queues["joiners"]["join_trip_weather"],
        ],
        em_queues["joiners"],
    )
    joiner_stations = JOINER_STATIONS.format(
        queues["joiners"]["stations"],
        queues["joiners"]["join_trip_stations"],
        em_queues["joiners"],
        queues["filters"]["filter_trip_stations"],
    )
    joiner_weather = JOINER_WEATHER.format(
        queues["joiners"]["weather"],
        queues["joiners"]["join_trip_weather"],
        em_queues["joiners"],
        queues["filters"]["filter_trip_weather"],
    )

    filters_pretoc, filters_year, filters_distance, em_filters = init_filters(
        amount_nodes
    )

    appliers_query1, appliers_query2, appliers_query3, em_appliers = init_appliers(
        amount_nodes
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


def init_filters(amount_nodes):
    filters_pretoc = ""
    for i in range(1, amount_nodes["filter_pretoc"] + 1):
        filters_pretoc += FILTER_PRETOC.format(i, i)

    filters_year = ""
    for i in range(1, amount_nodes["filter_year"] + 1):
        filters_year += FILTER_YEAR.format(i, i)

    filters_distance = ""
    for i in range(1, amount_nodes["filter_distance"] + 1):
        filters_year += FILTER_DISTANCE.format(i, i)

    em_filters = EM_FILTERS.format(
        [amount_nodes[k] for k in amount_nodes if "filter" in k]
    )

    return filters_pretoc, filters_year, filters_distance, em_filters


def init_appliers(amount_nodes):
    appliers_query1 = ""
    for i in range(1, amount_nodes["applier_query1"] + 1):
        appliers_query1 += APPLIER_QUERY1.format(i, i)

    appliers_query2 = ""
    for i in range(1, amount_nodes["applier_query2"] + 1):
        appliers_query2 += APPLIER_QUERY2.format(i, i)

    appliers_query3 = ""
    for i in range(1, amount_nodes["applier_query3"] + 1):
        appliers_query3 += APPLIER_QUERY3.format(i, i)

    em_appliers = EM_APPLIERS.format(
        [amount_nodes[k] for k in amount_nodes if "applier" in k]
    )

    return appliers_query1, appliers_query2, appliers_query3, em_appliers


if __name__ == "__main__":
    main()
