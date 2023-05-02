from common.connection import Connection
import time
from common.eof_manager import EOF_MSG
from common.utils import *

def main():
	EM_QUEUE = "eof_query_result_queue"
	RECEIVE_QUEUE = "query_result_queue"
	queries = ["query1", "query2", "query3"]

	conn = Connection()

	em_queue = conn.pubsub_queue(EM_QUEUE)
	recv_queue = conn.routing_queue(RECEIVE_QUEUE, queries)
	queries_done = set()

	def recv_query(ch, method, properties, body):
		msg = decode(body)

		if msg == EOF_MSG:
			print(f"Query terminada: {method.routing_key}")
			queries_done.add(method.routing_key)

			if len(queries_done) == len(queries):
				conn.stop_receiving()
		else:
			print(f"[{method.routing_key}] {msg}")

	def recv_eof(ch, method, properties, body):
		print('Recibido: EOF')
		for query in queries:
			recv_queue.send(EOF_MSG, routing_key=query)

	recv_queue.receive(recv_query)
	em_queue.receive(recv_eof)

	conn.start_receiving()
	conn.close()

if __name__ == "__main__":
	time.sleep(10)
	main()