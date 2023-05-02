from common.applier import ApplierController

def main():
	RECEIVE_QUEUE = "applier_2"
	SEND_QUEUE = "query_result_queue"
	EM_QUEUE = "eof_appliers_queue"
	op = lambda k,v: v[1] > 2*v[0]
	id_query = "query_2"

	def gen_result_msg(msg, applier):
		msg_splitted = msg.split(',')
		key = msg_splitted[0]
		value = [int(i) for i in msg_splitted[1:]]

		result = applier.apply(key, value)

		return result, msg

	ApplierController(RECEIVE_QUEUE, EM_QUEUE, SEND_QUEUE, op, gen_result_msg, id_query)