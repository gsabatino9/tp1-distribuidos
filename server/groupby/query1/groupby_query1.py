from server.groupby.common.groupby_controller import GroupbyController


class GroupbyQuery1:
    def __init__(self, name_recv_queue, name_em_queue, name_send_queue):
        operation = lambda old, new: [old[0] + max(new, 0), old[1] + 1]
        base_data = [0, 0]

        self.groupby_controller = GroupbyController(
            name_recv_queue,
            name_em_queue,
            name_send_queue,
            operation,
            base_data,
            self.gen_key_value,
        )

    def gen_key_value(self, trip):
        return trip[0], float(trip[1])

    def stop(self):
        self.groupby_controller.stop()
