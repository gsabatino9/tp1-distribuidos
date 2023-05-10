from data_router import DataRouter
import os

ID = os.environ.get('ID')
NAME_RECV_QUEUE = 'data_router_q'
NAME_STATIONS_QUEUE = 'joiner_stations_q'
NAME_WEATHER_QUEUE = 'joiner_weather_q'
NAME_EM_QUEUE = 'eof_manager_q'
NAME_JOIN_STATIONS_QUEUE = 'join_trip_stations_q'
NAME_JOIN_WEATHER_QUEUE = 'join_trip_weather_q'

def main():
	d = DataRouter(int(ID), NAME_RECV_QUEUE, NAME_STATIONS_QUEUE, NAME_WEATHER_QUEUE, NAME_EM_QUEUE, NAME_JOIN_STATIONS_QUEUE, NAME_JOIN_WEATHER_QUEUE)
	d.stop()

if __name__ == "__main__":
	main()