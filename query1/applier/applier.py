from common.applier import ApplierController

def main():
	RECEIVE_QUEUE = "applier_1"
	SEND_QUEUE = "query_result_queue"
	EM_QUEUE = "eof_appliers_queue"
	op = lambda k,v: [k, str(v[1]/v[0])]
	id_query = "query_1"

	def gen_result_msg(msg, applier):
		msg_splitted = msg.split(',')
		key = msg_splitted[0]
		value = [float(i) for i in msg_splitted[1:]]

		result = applier.apply(key, value)
		msg_to_send = ','.join(result)

		return result, msg_to_send

	ApplierController(RECEIVE_QUEUE, EM_QUEUE, SEND_QUEUE, op, gen_result_msg, id_query)