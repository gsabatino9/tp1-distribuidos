from common.connection import Connection
from common.eof_manager import EOF_MSG, WORKER_DONE_MSG
from common.utils import *
import random

class EOFManager:
	def __init__(self, name_recv_queue, name_next_em_queue):
		self.workers = {}
		self.__connect(name_recv_queue, name_next_em_queue)

	def __connect(self, name_recv_queue, name_next_em_queue):
		self.conn = Connection()

		self.em_queue = self.conn.pubsub_queue(name_recv_queue)
		if name_next_em_queue:
			self.next_em_queue = self.conn.pubsub_queue(name_next_em_queue)

		self.em_queue.receive(self.process_message)
		self.conn.start_receiving()

	def process_message(self, ch, method, properties, body):
		msg = decode(body)

		if msg == EOF_MSG:
			self.__eof_arrived()
		elif msg == WORKER_DONE_MSG:
			self.__worker_done()
		else:
			self.__register_worker(msg)

	def __register_worker(self, msg):
		print(f'New worker: {msg}')
		if msg in self.workers:
			queue, value = self.workers[msg]
			self.workers[msg] = (queue, value+1)
		else:
			queue = self.conn.basic_queue(msg)
			self.workers[msg] = (queue, 1)

	def __worker_done(self):
		print('Worker done')
		if not self.__all_workers_done():
			self.__close_worker()
		else:
			self.__send_eof_next_stage()
			self.stop()

	def __eof_arrived(self):
		print('eof arrived')
		self.__close_worker()

	def __send_eof_next_stage(self):
		if hasattr(self, "next_em_queue"):
			print('Mandando eof next stage')
			self.next_em_queue.send(EOF_MSG)

	def __close_worker(self):
		worker = self.__pick_worker()
		queue, value = self.workers.pop(worker)
		print(f'Closing worker: {worker}, {value}')
		queue.send(EOF_MSG)

		if value > 1:
			self.workers[worker] = (queue, value-1)

	def __pick_worker(self):
		return random.choice(list(self.workers.keys()))

	def __all_workers_done(self):
		return len(self.workers) == 0

	def stop(self):
		self.conn.close()