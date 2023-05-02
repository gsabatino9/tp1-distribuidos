from common.connection import Connection
import sys, os
from common.eof_manager import EOF_MSG, WORKER_DONE_MSG
from common.utils import *

LAST_STATION = "last"

class StaticDataHandler:
    def __init__(self, idx_code, idx_yearid, len_msg):
        self.stations = {}
        self.idx_code = idx_code
        self.idx_yearid = idx_yearid
        self.idxs_joined_data = []

        for i in range(len_msg):
            if i != idx_code and i != idx_yearid:
                self.idxs_joined_data.append(i)

    def add_station(self, station):
        code, yearid = station[self.idx_code], station[self.idx_yearid]
        self.stations[code, yearid] = [elem for i,elem in enumerate(station) if i in self.idxs_joined_data]

    def join_trip(self, start_code, end_code, yearid):
        """
        Le retorno: 
        name_start_station, lat_start_station, long_start_station,
        name_end_station, lat_end_station, long_end_station
        """
        start_station = self.__join_trip(start_code, yearid)
        end_station = self.__join_trip(end_code, yearid)

        return ','.join(start_station+end_station)

    def __join_trip(self, code, yearid):
        return self.stations[code, yearid]

class StationsHandler:
    def __init__(self, recv_static_data_queue, recv_trips_queue, em_queue, send_joined_trip_queue, len_msg):
        self.__create_static_data(len_msg)
        self.__connect(recv_static_data_queue, recv_trips_queue, em_queue, send_joined_trip_queue)
        self.recv_queue.receive(self.proccess_message)
        
        print("[stations_handler] listo para recibir")
        self.connection.start_receiving()

    def __create_static_data(self, len_msg):
        self.montreal = StaticDataHandler(0, 4, len_msg)
        self.toronto = StaticDataHandler(0, 4, len_msg)
        self.washington = StaticDataHandler(0, 4, len_msg)

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
        if msg == LAST_STATION:
            self.__last_station_arrived()
        else:
            print(msg)
            self.__station_arrived(msg)

    def __station_arrived(self, msg):
        city, station = split_city(msg)
        self.__add_station(city, station)

    def __add_station(self, city, station):
        if city == "Montreal":
            self.montreal.add_station(station)
        elif city == "Toronto":
            self.toronto.add_station(station)
        else:
            self.washington.add_station(station)

    def __last_station_arrived(self):
        self.recv_trips_queue.receive(self.proccess_trip_arrived)

    def __eof_arrived(self):
        self.connection.stop_receiving()
        self.em_queue.send(WORKER_DONE_MSG)
        self.close()

    def proccess_trip_arrived(self, ch, method, properties, body):
        msg = decode(body)

        if msg == EOF_MSG:
            self.__eof_arrived()
        else:
            self.__trip_arrived(msg)

    def __trip_arrived(self, msg):
        station_joined = self.__join_trip(msg)
        self.send_joined_trip_queue.send(msg+','+station_joined)

    def __join_trip(self, data):
        city, trip = split_city(data)
        return self.__join_trip_by_city(city, trip)

    def __join_trip_by_city(self, city, trip):
        start_code, end_code, yearid = trip[1], trip[3], trip[-1]

        if city == "Montreal":
            return self.montreal.join_trip(start_code, end_code, yearid)
        elif city == "Toronto":
            return self.toronto.join_trip(start_code, end_code, yearid)
        else:
            return self.washington.join_trip(start_code, end_code, yearid)

    def close(self):
        print('[stations_handler] close: success')
        self.connection.close()