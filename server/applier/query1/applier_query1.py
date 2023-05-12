from server.queue.connection import Connection
from server.applier.common.applier import Applier
from server.common.utils_messages_client import decode, is_eof
from server.common.utils_messages_eof import ack_msg

class ApplierQuery1:
	def __init__(self, name_recv_queue, name_em_queue, name_send_queue):
		operation = lambda k,v: [k, str(v[0]/v[1])]
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
			result, msg_to_send = self.__gen_result_msg(trip)
			if result:
				result_trips.append(msg_to_send)

	def __gen_result_msg(self, trip):
		key = trip[0]
		value = [float(i) for i in trip[1:]]

		result = self.applier.apply(key, value)
		msg_to_send = ','.join(result)

		return result, msg_to_send

	def __eof_arrived(self):
		print("Eof llegó")
