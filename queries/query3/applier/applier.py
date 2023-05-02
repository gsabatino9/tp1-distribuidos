from common.applier import ApplierController

def main():
	RECEIVE_QUEUE = "applier_3"
	SEND_QUEUE = "query_result_queue"
	EM_QUEUE = "eof_appliers_queue"
	op = lambda k,v: (v[1]/v[0] >= 6) if v[0] > 0 else False
	id_query = "query_3"

	def gen_result_msg(msg, applier):
		msg_splitted = msg.split(',')
		key = msg_splitted[0]
		value = [float(i) for i in msg_splitted[1:]]

		result = applier.apply(key, value)

		return result, key

	ApplierController(RECEIVE_QUEUE, EM_QUEUE, SEND_QUEUE, op, gen_result_msg, id_query)