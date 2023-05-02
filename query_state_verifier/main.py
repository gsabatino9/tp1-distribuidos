from common.connection import Connection
import time
from common.eof_manager import EOF_MSG
from common.utils import *

def main():
	time.sleep(10)
	RECEIVE_QUEUE = "query_result_queue"
	EM_QUEUE = "eof_query_result_queue"
	types_messages = ["query1", "query2"]

	conn = Connection()
	recv_queue = conn.routing_queue(RECEIVE_QUEUE, types_messages)
	queries_done = set()

	def callback(ch, method, properties, body):
		msg = decode(body)

		if msg == EOF_MSG:
			print(f"Query terminada: {method.routing_key}")
			queries_done.add(method.routing_key)

			if len(queries_done) == len(types_messages):
				conn.stop_receiving()
		else:
			print(f"[{method.routing_key}] {msg}")

	recv_queue.receive(callback)

	conn.start_receiving()
	conn.close()

if __name__ == "__main__":
	main()