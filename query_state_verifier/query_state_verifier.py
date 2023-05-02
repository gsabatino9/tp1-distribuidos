from common.connection import Connection
import time
from common.eof_manager import EOF_MSG
from common.utils import *

class QueryStateVerifier:
	def __init__(self, recv_queue, em_queue, queries):
		self.queries_done = set()
		self.queries = queries
		self.queries_results = {i:[] for i in queries}
		self.__connect(recv_queue, em_queue, queries)
		
	def __connect(self, recv_queue, em_queue, queries):
		self.connection = Connection()
		self.em_queue = self.connection.pubsub_queue(em_queue)
		self.recv_queue = self.connection.routing_queue(recv_queue, queries)

		self.recv_queue.receive(self.recv_query)
		self.em_queue.receive(self.recv_eof)

		self.connection.start_receiving()

	def __all_queries_end(self):
		return len(self.queries_done) == len(self.queries)

	def recv_query(self, ch, method, properties, body):
		msg = decode(body)
		query = method.routing_key

		if msg == EOF_MSG:
			print(f"Query terminada: {query}")
			self.queries_done.add(query)

			if self.__all_queries_end():
				print(f"Todas las queries terminadas.")
				self.connection.close()
		else:
			print(f"[{method.routing_key}] {msg}")

	def recv_eof(self, ch, method, properties, body):
		print('Recibido: EOF')
		for query in self.queries:
			self.recv_queue.send(EOF_MSG, routing_key=query)