from server.applier.common.applier_controller import ApplierController

class ApplierQuery3:
	def __init__(self, name_recv_queue, name_em_queue, name_send_queue):
		operation = lambda k,v: (v[1]/v[0] >= 6) if v[0] > 0 else False
		self.applier_controller = ApplierController(name_recv_queue, name_em_queue, name_send_queue, operation, self.gen_result_msg)

	def gen_result_msg(self, trip, applier):
		key = trip[0]
		value = [float(i) for i in trip[1:]]

		result = applier.apply(key, value)

		return result, key

	def stop(self):
		self.applier_controller.stop()
