from joiner_weather import JoinerWeather
import os

NAME_RECV_QUEUE = 'joiner_weather_q'
NAME_TRIPS_QUEUE = 'join_trip_weather_q'
NAME_EM_QUEUE = 'eof_manager_q'
NAME_NEXT_STAGE_QUEUE = 'filter_joined_weather_q'

def main():
	j = JoinerWeather(NAME_RECV_QUEUE, NAME_TRIPS_QUEUE, NAME_EM_QUEUE, NAME_NEXT_STAGE_QUEUE)
	j.stop()

if __name__ == "__main__":
	main()