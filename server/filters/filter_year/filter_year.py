from server.queue.connection import Connection
from server.filters.common.utils import ack_msg
from server.common.utils_messages_client import decode, is_eof
from server.filters.common.filter import Filter

class FilterYear:
	def __init__(self, name_recv_exchange, name_recv_queue, name_em_queue):
		self.not_filtered = 0
		self.__init_filter()
		self.__connect(name_recv_exchange, name_recv_queue, name_em_queue)
		self.recv_queue.receive(self.proccess_message)
		self.queue_connection.start_receiving()

	def __init_filter(self):
		columns_names = """start_date,start_station_code,end_date,end_station_code,duration_sec,is_member,yearid,name_start_station,lat_start_station,long_start_station,name_end_station,lat_end_station,long_end_station"""
		reduced_columns = "yearid,name_start_station"

		self.filter = Filter(columns_names, reduced_columns, {"yearid": lambda x: int(x) in [2016, 2017]})

	def __connect(self, name_recv_exchange, name_recv_queue, name_em_queue):
		self.queue_connection = Connection()
		self.recv_queue = self.queue_connection.pubsub_worker_queue(name_recv_exchange, name_recv_queue)
		self.em_queue = self.queue_connection.pubsub_queue(name_em_queue)

	def proccess_message(self, ch, method, properties, body):
		if is_eof(body):
			self.__eof_arrived(ch)
		else:
			self.__filter(body)

	def __filter(self, body):
		header, joined_trips = decode(body)
		trips_to_next_stage = []

		for trip in joined_trips:
			new_trip = self.filter.apply(trip)
			if new_trip:
				self.not_filtered += 1
				trips_to_next_stage.append(trip)

	def __eof_arrived(self, ch):
		ch.stop_consuming()
		print("EOF llegó a filtro - not_filtered", self.not_filtered)
		self.em_queue.send(ack_msg())

	def stop(self):
		self.queue_connection.close()