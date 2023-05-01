from common.filter import FilterColumns, FilterRows, Transformer
from common.connection import Connection
from common.eof_manager import EOFManager, EOF_MSG, REGISTER_EOF_MSG

class TripTransformer:
	def __init__(self, columns_names, wanted_columns, filter_conditions):
		self.filter_columns = FilterColumns(columns_names, wanted_columns)
		#self.transformer = Transformer(wanted_columns, transform_conditions)
		self.filter_rows = FilterRows(wanted_columns, filter_conditions)

	def apply(self, trip):
		transf_trip = self.filter_columns.filter(trip)
		#transf_trip = self.transformer.transform(transf_trip)
		
		if self.filter_rows.filter(transf_trip):
			return transf_trip
		else: return None

class TripsTransformer:
	def __init__(self, recv_queue, transformers, send_queues):
		self.transformers = transformers
		self.__connect(recv_queue, send_queues)

		print("[trips_transformer] listo para recibir")
		self.connection.start_receiving()

	def __connect(self, recv_queue, send_queues):
		self.connection = Connection()
		self.recv_queue = self.connection.basic_queue(recv_queue)
		self.recv_queue.receive(self.recv_trip)
		self.queues = []

		for send_queue in send_queues:
			queue = self.connection.basic_queue(send_queue)
			self.queues.append(queue)

		self.eof_manager = EOFManager(self.queues)

	def recv_trip(self, ch, method, properties, body):
		trip = body.decode('utf-8')

		if self.eof_manager.is_eof(trip): return
		
		for i, transformer in enumerate(self.transformers):
			transf_trip = transformer.apply(trip)
			if transf_trip:
				self.queues[i].send(transf_trip)
				print(transf_trip)

