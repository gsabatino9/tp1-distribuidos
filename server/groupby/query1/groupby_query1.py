from server.queue.connection import Connection
from server.groupby.common.groupby import Groupby
from server.groupby.common.utils import ack_msg, construct_msg
from server.common.utils_messages_client import decode, is_eof

class GroupbyQuery1:
	def __init__(self, name_recv_queue, name_em_queue, name_send_queue):
		operation = lambda old, new: [old[0]+max(new,0), old[1]+1]
		base_data = [0,0]

		self.groupby = Groupby(operation, base_data)

		self.__connect(name_recv_queue, name_em_queue, name_send_queue)
		self.recv_queue.receive(self.process_messages)
		self.connection.start_receiving()

	def __connect(self, name_recv_queue, name_em_queue, name_send_queue):
		self.connection = Connection()
		self.recv_queue = self.connection.basic_queue(name_recv_queue)
		self.send_queue = self.connection.basic_queue(name_send_queue)
		self.em_queue = self.connection.pubsub_queue(name_em_queue)

	def process_messages(self, ch, method, properties, body):
		if is_eof(body):
			self.__eof_arrived()
		else:
			self.__data_arrived(body)

	def __data_arrived(self, body):
		header, filtered_trips = decode(body)

		for trip in filtered_trips:
			trip = trip.split(',')
			key, value = self.__gen_key_value(trip)
			self.groupby.add_data(key, value)

	def __gen_key_value(self, trip):
		return trip[0], float(trip[1])

	def __eof_arrived(self):
		self.__send_to_apply()
		self.em_queue.send(ack_msg())

	def __send_to_apply(self):
		#grouped_trips = []

		for key in self.groupby.grouped_data:
			value = self.groupby.grouped_data[key]
			to_append = f"{key},{value[0]},{value[1]}"
			#grouped_trips.append(to_append)

			msg = construct_msg([to_append])
			self.send_queue.send(msg)
