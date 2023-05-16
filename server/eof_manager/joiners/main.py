from common.eof_manager import EOFManager
import os

NAME_RECV_QUEUE = "eof_manager_joiners_q"
NAME_SEND_QUEUE = "eof_manager_filters_q"
NAME_STATIONS_QUEUE = "joiner_stations_q"
NAME_WEATHER_QUEUE = "joiner_weather_q"
NAME_JOIN_STATIONS_QUEUE = "join_trip_stations_q"
NAME_JOIN_WEATHER_QUEUE = "join_trip_weather_q"


def main():
    e = EOFManager(
        NAME_RECV_QUEUE,
        NAME_SEND_QUEUE,
        NAME_STATIONS_QUEUE,
        NAME_WEATHER_QUEUE,
        NAME_JOIN_STATIONS_QUEUE,
        NAME_JOIN_WEATHER_QUEUE,
    )
    e.stop()


if __name__ == "__main__":
    main()
