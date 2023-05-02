from static_data_receiver import StaticDataReceiver
from trips_receiver import TripsReceiver
import time

HOST = 'receiver'
PORT_STATIC = 12345
STATIONS_QUEUE = "stations_queue"

PORT_TRIPS = 12346
TRIPS_QUEUE = "trips_queue"
JOIN_TRIPS_STATIONS_QUEUE = "join_trip_station_queue"
EM_QUEUE = "eof_handler_queue"

def main():
    StaticDataReceiver(HOST, PORT_STATIC, STATIONS_QUEUE)
    TripsReceiver(HOST, PORT_TRIPS, [TRIPS_QUEUE, JOIN_TRIPS_STATIONS_QUEUE], EM_QUEUE)

if __name__ == "__main__":
    time.sleep(10)
    main()