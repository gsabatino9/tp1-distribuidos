from common.connection import Connection
import sys, os
from common.eof_manager import EOF_MSG, WORKER_DONE_MSG
from common.utils import *

LAST_WEATHER = "last"

class StaticDataHandler:
    def __init__(self, idx_date, len_msg):
        self.weathers = {}
        self.idx_date = idx_date
        self.idxs_joined_data = []

        for i in range(len_msg):
            if i != idx_date:
                self.idxs_joined_data.append(i)

    def add_weather(self, weather):
        date = weather[self.idx_date]
        self.weathers[date] = [elem for i,elem in enumerate(weather) if i in self.idxs_joined_data]

    def join_trip(self, start_date, end_date):
        start_weather = self.__join_trip(start_date)
        end_weather = self.__join_trip(end_date)

        return ','.join(start_weather+end_weather)

    def __join_trip(self, date):
        return self.weathers[date]

class WeatherHandler:
    def __init__(self, recv_static_data_queue, recv_trips_queue, em_queue, send_joined_trip_queue, len_msg):
        self.__create_static_data(len_msg)
        self.__connect(recv_static_data_queue, recv_trips_queue, em_queue, send_joined_trip_queue)
        self.recv_queue.receive(self.proccess_message)
        
        print("[weather_handler] listo para recibir")
        self.connection.start_receiving()

    def __create_static_data(self, len_msg):
        self.montreal = StaticDataHandler(0, len_msg)
        self.toronto = StaticDataHandler(0, len_msg)
        self.washington = StaticDataHandler(0, len_msg)

    def __connect(self, recv_static_data_queue, recv_trips_queue, em_queue, send_joined_trip_queue):
        self.connection = Connection()
        self.recv_queue = self.connection.basic_queue(recv_static_data_queue)
        self.recv_trips_queue = self.connection.basic_queue(recv_trips_queue)
        # es un worker en vez de un basic_queue
        self.send_joined_trip_queue = self.connection.basic_queue(send_joined_trip_queue)

        self.__connect_to_eof_manager(em_queue, recv_trips_queue)

    def __connect_to_eof_manager(self, em_queue, recv_trips_queue):
        self.em_queue = self.connection.pubsub_queue(em_queue)
        self.em_queue.send(recv_trips_queue) # le digo de dónde espero el eof

    def proccess_message(self, ch, method, properties, body):
        msg = decode(body)
        if msg == LAST_WEATHER:
            self.__last_weather_arrived()
        else:
            self.__weather_arrived(msg)

    def __weather_arrived(self, msg):
        city, weather = split_city(msg)
        self.__add_weather(city, weather)

    def __add_weather(self, city, weather):
        if city == "Montreal":
            self.montreal.add_weather(weather)
        elif city == "Toronto":
            self.toronto.add_weather(weather)
        else:
            self.washington.add_weather(weather)

    def __last_weather_arrived(self):
        self.recv_trips_queue.receive(self.proccess_trip_arrived, auto_ack=False)

    def __eof_arrived(self, ch, delivery_tag):
        self.connection.stop_receiving()
        self.em_queue.send(WORKER_DONE_MSG)
        ch.basic_ack(delivery_tag = delivery_tag)
        self.close()

    def proccess_trip_arrived(self, ch, method, properties, body):
        msg = decode(body)

        if msg == EOF_MSG:
            self.__eof_arrived(ch, method.delivery_tag)
        else:
            self.__trip_arrived(msg, ch, method.delivery_tag)

    def __trip_arrived(self, msg, ch, delivery_tag):
        weather_joined = self.__join_trip(msg)
        self.send_joined_trip_queue.send(msg+','+weather_joined)
        ch.basic_ack(delivery_tag = delivery_tag)

    def __join_trip(self, data):
        city, trip = split_city(data)
        return self.__join_trip_by_city(city, trip)

    def __join_trip_by_city(self, city, trip):
        start_date, end_date = trip[0], trip[2]

        if city == "Montreal":
            return self.montreal.join_trip(start_date, end_date)
        elif city == "Toronto":
            return self.toronto.join_trip(start_date, end_date)
        else:
            return self.washington.join_trip(start_date, end_date)

    def close(self):
        print('[weather_handler] close: success')
        self.connection.close()