from server.common.queue.connection import Connection
from server.common.utils_messages_eof import ack_msg
from server.common.utils_messages_group import decode, is_eof

class ResultsVerifier:
	def __init__(self, name_recv_queue, name_em_queue):
		self.queries_results = {i:[] for i in range(1,4)}
		self.queries_ended = {i:False for i in range(1,4)}
		self.__connect(name_recv_queue, name_em_queue)
		self.recv_queue.receive(self.process_messages)
		self.conn.start_receiving()

	def __connect(self, name_recv_queue, name_em_queue):
		self.conn = Connection()
		self.recv_queue = self.conn.routing_queue(name_recv_queue, routing_keys=["1", "2", "3"])
		self.em_queue = self.conn.pubsub_queue(name_em_queue)

	def process_messages(self, ch, method, properties, body):
		id_query = int(method.routing_key)
		if is_eof(body):
			print("eof recv")
			self.__eof_arrived(id_query)
		else:
			self.__query_result_arrived(body, id_query)
	
	def __query_result_arrived(self, body, id_query):
		header, results = decode(body)
		self.queries_results[id_query] += results
		
	def __eof_arrived(self, id_query):
		self.em_queue.send(ack_msg())
		self.queries_ended[id_query] = True

		self.__verify_last_result()

	def __verify_last_result(self):
		ended = True
		for query in self.queries_ended:
			if not self.queries_ended[query]:
				ended = False

		if ended:
			print(f"Llegó un eof - {self.queries_results}")
