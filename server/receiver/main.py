from receiver import Receiver
import os

HOST = 'receiver'
PORT = 12345
NAME_STATIONS_QUEUE = 'joiner_stations_q'
NAME_WEATHER_QUEUE = 'joiner_weather_q'
NAME_TRIPS_QUEUES = ['join_trip_weather_q', 'join_trip_stations_q']
NAME_EM_QUEUE = 'eof_manager_q'

def main():
	receiver = Receiver(HOST, PORT, NAME_STATIONS_QUEUE, NAME_WEATHER_QUEUE, NAME_TRIPS_QUEUES, NAME_EM_QUEUE)
	receiver.run()
	receiver.stop()

if __name__ == "__main__":
	main()