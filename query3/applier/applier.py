from common.applier import Applier
from common.connection import Connection
from common.eof_manager import EOF_MSG, WORKER_DONE_MSG
from common.utils import *

class ApplierController:
	def __init__(self, recv_queue, em_queue, send_queue):
		op = lambda k,v: v[1]/v[0] >= 6
		self.applier = Applier(op)

		self.conn = Connection()
		self.recv_queue = self.conn.basic_queue(recv_queue)
		self.send_queue = self.conn.routing_queue(send_queue)

		self.em_queue = self.conn.pubsub_queue(em_queue)
		self.em_queue.send(recv_queue)

		self.recv_queue.receive(self.recv_data_to_apply)
		self.conn.start_receiving()

	def recv_data_to_apply(self, ch, method, properties, body):
		msg = decode(body)
		if msg == EOF_MSG:
			self.__eof_arrived()
		else:
			self.__apply(msg)

	def __eof_arrived(self):
		self.conn.stop_receiving()
		#self.send_queue.send(EOF_MSG, routing_key="query1")
		self.em_queue.send(WORKER_DONE_MSG)
		
	def __apply(self, msg):
		msg_splitted = msg.split(',')
		key = msg_splitted[0]
		value = [float(i) for i in msg_splitted[1:]]

		result = self.applier.apply(key, value)
		if result:
			self.send_queue.send(key, routing_key="query3")

def main():
	RECEIVE_QUEUE = "applier_3"
	SEND_QUEUE = "query_result_queue"
	EM_QUEUE = "eof_appliers_queue"

	ApplierController(RECEIVE_QUEUE, EM_QUEUE, SEND_QUEUE)