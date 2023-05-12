from server.common.queue.connection import Connection
from server.applier.common.applier import Applier
from server.common.utils_messages_eof import ack_msg
from server.common.utils_messages_group import decode, is_eof

class ApplierController:
	def __init__(self, name_recv_queue, name_em_queue, name_send_queue, operation, gen_result_msg):
		self.gen_result_msg = gen_result_msg
		self.applier = Applier(operation)
		self.__connect(name_recv_queue, name_em_queue, name_send_queue)
		self.recv_queue.receive(self.process_messages)
		self.conn.start_receiving()

	def __connect(self, name_recv_queue, name_em_queue, name_send_queue):
		self.conn = Connection()
		self.recv_queue = self.conn.basic_queue(name_recv_queue)
		self.send_queue = self.conn.routing_queue(name_send_queue)

		self.em_queue = self.conn.pubsub_queue(name_em_queue)

	def process_messages(self, ch, method, properties, body):
		if is_eof(body):
			self.__eof_arrived()
		else:
			self.__apply(body)
	
	def __apply(self, body):
		header, agrouped_trips = decode(body)
		result_trips = []

		for trip in agrouped_trips:
			trip = trip.split(',')
			result, msg_to_send = self.gen_result_msg(trip, self.applier)
			if result:
				result_trips.append(msg_to_send)

		#print(result_trips)

	def __eof_arrived(self):
		print("Eof llegó")