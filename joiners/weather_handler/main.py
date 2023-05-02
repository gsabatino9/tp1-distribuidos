from weather_handler import WeatherHandler
import time

RECV_QUEUE = "weather_queue"
RECV_TRIPS_QUEUE = "join_trip_weather_queue"
SEND_TRIPS_QUEUE = "trips_weather_queue"
EM_QUEUE = "eof_handler_queue"
LEN_MSG = 10

if __name__ == "__main__":
    time.sleep(11)
    WeatherHandler(RECV_QUEUE, RECV_TRIPS_QUEUE, EM_QUEUE, SEND_TRIPS_QUEUE, LEN_MSG)