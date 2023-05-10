from joiner_weather import JoinerWeather
import os

NAME_RECV_QUEUE = 'joiner_weather_q'
NAME_TRIPS_QUEUE = 'join_trip_weather_q'

def main():
	j = JoinerWeather(NAME_RECV_QUEUE, NAME_TRIPS_QUEUE)
	j.stop()

if __name__ == "__main__":
	main()