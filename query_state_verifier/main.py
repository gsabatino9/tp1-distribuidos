from common.connection import Connection
import time
from common.eof_manager import EOF_MSG, WORKER_DONE_MSG
from common.utils import *

def main():
	time.sleep(10)
	RECEIVE_QUEUE = "query_result_queue"
	EM_QUEUE = "eof_query_result_queue"

	conn = Connection()
	recv_queue = conn.basic_queue(RECEIVE_QUEUE)
	em_queue = conn.pubsub_queue(EM_QUEUE)
	em_queue.send(RECEIVE_QUEUE)

	def callback(ch, method, properties, body):
		msg = decode(body)

		if msg == EOF_MSG:
			print('Todas las queries terminadas.')
			conn.stop_receiving()
			em_queue.send(WORKER_DONE_MSG)
		else:
			#key, val_2016, val_2017 = msg.split(',')
			print(f"[Query] {msg}")

	recv_queue.receive(callback)

	conn.start_receiving()
	conn.close()

if __name__ == "__main__":
	main()