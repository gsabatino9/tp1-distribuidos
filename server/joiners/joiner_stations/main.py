from joiner_stations import JoinerStations
import os

NAME_RECV_QUEUE = 'joiner_stations_q'
NAME_TRIPS_QUEUE = 'join_trip_stations_q'
NAME_EM_QUEUE = 'eof_manager_q'

def main():
	j = JoinerStations(NAME_RECV_QUEUE, NAME_TRIPS_QUEUE, NAME_EM_QUEUE)
	j.stop()

if __name__ == "__main__":
	main()