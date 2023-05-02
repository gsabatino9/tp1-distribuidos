from static_data_receiver import StaticDataReceiver
from trips_receiver import TripsReceiver
from common.utils import initialize_log, initialize_config
import time, os, logging

HOST = os.environ['HOST']
PORT_STATIC = int(os.environ['PORT_STATIC'])
STATIONS_QUEUE = os.environ['STATIONS_QUEUE']
WEATHER_QUEUE = os.environ['WEATHER_QUEUE']

PORT_TRIPS = int(os.environ['PORT_TRIPS'])
TRIPS_QUEUE = os.environ['TRIPS_QUEUE']
JOIN_TRIPS_STATIONS_QUEUE = os.environ['JOIN_TRIPS_STATIONS_QUEUE']
JOIN_TRIPS_WEATHER_QUEUE = os.environ['JOIN_TRIPS_WEATHER_QUEUE']
EM_QUEUE = os.environ['EM_QUEUE']

def main():
	initialize_log()
	logging.info(f"action: server_up | result: success | Host: {HOST} | Ports: {PORT_STATIC},{PORT_TRIPS}")

	StaticDataReceiver(HOST, PORT_STATIC, STATIONS_QUEUE, WEATHER_QUEUE)
	TripsReceiver(HOST, PORT_TRIPS, [TRIPS_QUEUE, JOIN_TRIPS_STATIONS_QUEUE, JOIN_TRIPS_WEATHER_QUEUE], EM_QUEUE)

if __name__ == "__main__":
	time.sleep(10)
	main()