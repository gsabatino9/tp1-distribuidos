from stations_handler import StationsHandler
import time

RECV_QUEUE = "stations_queue"
RECV_TRIPS_QUEUE = "join_trip_station_queue"
SEND_TRIPS_QUEUE = "trips_stations_queue"
EM_QUEUE = "eof_handler_queue"
LEN_MSG = 5

if __name__ == "__main__":
    time.sleep(11)
    StationsHandler(RECV_QUEUE, RECV_TRIPS_QUEUE, EM_QUEUE, SEND_TRIPS_QUEUE, LEN_MSG)