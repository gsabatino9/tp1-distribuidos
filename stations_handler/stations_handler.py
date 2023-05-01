from common.connection import Connection
from common.eof_manager import EOFManager, EOF_MSG, REGISTER_EOF_MSG
import sys, os

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
    def __init__(self, recv_static_data_queue, recv_trips_queue, send_joined_trip_queue, len_msg):
        self.static_data = StaticDataHandler(0, 4, len_msg)
        self.__connect(recv_static_data_queue, recv_trips_queue, send_joined_trip_queue)
        self.eof_manager = EOFManager([self.send_joined_trip_queue])
        self.recv_queue.receive(self.proccess_message)
        
        print("[stations_handler] listo para recibir")
        self.connection.start_receiving()

    def __connect(self, recv_static_data_queue, recv_trips_queue, send_joined_trip_queue):
        self.connection = Connection()
        self.recv_queue = self.connection.basic_queue(recv_static_data_queue)
        self.recv_trips_queue = self.connection.basic_queue(recv_trips_queue)
        # es un worker en vez de un basic_queue
        self.send_joined_trip_queue = self.connection.basic_queue(send_joined_trip_queue)

    def proccess_message(self, ch, method, properties, body):
        msg = body.decode('utf-8')
        if msg == LAST_STATION:
            self.__last_station_arrived()
        elif not self.eof_manager.is_eof(msg):
            self.__station_arrived(msg)

    def __station_arrived(self, msg):
        station = msg.split(',')
        self.static_data.add_station(station)

    def __last_station_arrived(self):
        self.recv_trips_queue.receive(self.proccess_trip_arrived)

    def proccess_trip_arrived(self, ch, method, properties, body):
        msg = body.decode('utf-8')

        if not self.eof_manager.is_eof(msg):
            trip = msg.split(',')
            station_joined = self.static_data.join_trip(trip[1], trip[3], trip[-1])

            self.send_joined_trip_queue.send(msg+','+station_joined)