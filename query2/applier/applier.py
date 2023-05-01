from common.applier import Applier
from common.connection import Connection

def main():
	RECEIVE_QUEUE = "applier_2"

	conn = Connection()
	recv_queue = conn.basic_queue(RECEIVE_QUEUE)

	op = lambda k,v: [k, v[1] > 2*v[0]]
	double_checker = Applier(op)

	def callback(ch, method, properties, body):
		msg = body.decode('utf-8').split(',')
		key = msg[0]
		value = [int(i) for i in msg[1:]]

		result = double_checker.apply(key, value)
		print(f'{msg} Pasa filtro: {result}')

	recv_queue.receive(callback)

	conn.start_receiving()
	conn.close()