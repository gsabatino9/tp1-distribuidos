EOF_MSG = "EOF"
REGISTER_EOF_MSG = "REGISTER_EOF"

class EOFManager:
	def __init__(self, send_queues):
		self.eof_to_wait = 0
		self.eof_received = 0
		self.send_queues = send_queues

		for queue in send_queues:
			queue.send(REGISTER_EOF_MSG)

	def __register_eof(self):
		print('Llegó register')
		self.eof_to_wait += 1

	def __add_eof(self):
		print('Llegó eof')
		self.eof_received = max(self.eof_received+1, self.eof_to_wait)
		
		if self.eof_received == self.eof_to_wait:
			print('Mando eof')
			for queue in self.send_queues:
				queue.send(EOF_MSG)

	def is_eof(self, msg):
		if msg == EOF_MSG:
			self.__add_eof()
			return True
		elif msg == REGISTER_EOF_MSG:
			self.__register_eof()
			return True
		else:
			return False

	def all_eof_received(self):
		return self.eof_received == self.eof_to_wait
