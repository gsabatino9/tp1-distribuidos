import signal, sys
from server.common.queue.connection import Connection
from server.groupby.common.groupby import Groupby
from server.common.utils_messages_client import decode, is_eof
from server.common.utils_messages_eof import ack_msg
from server.common.utils_messages_group import construct_msg


class GroupbyController:
    def __init__(
        self,
        name_recv_queue,
        name_em_queue,
        name_send_queue,
        operation,
        base_data,
        gen_key_value,
    ):
        self.__init_groupby(operation, base_data, gen_key_value)

        self.__connect(name_recv_queue, name_em_queue, name_send_queue)
        self.recv_queue.receive(self.process_messages)
        self.queue_connection.start_receiving()

    def __init_groupby(self, operation, base_data, gen_key_value):
        self.running = True
        signal.signal(signal.SIGTERM, self.stop)

        self.groupby = Groupby(operation, base_data)
        self.gen_key_value = gen_key_value
        print("action: groupby_started | result: success")

    def __connect(self, name_recv_queue, name_em_queue, name_send_queue):
        self.queue_connection = Connection()
        self.recv_queue = self.queue_connection.basic_queue(name_recv_queue)
        self.send_queue = self.queue_connection.basic_queue(name_send_queue)
        self.em_queue = self.queue_connection.pubsub_queue(name_em_queue)

    def process_messages(self, ch, method, properties, body):
        if is_eof(body):
            self.__eof_arrived()
        else:
            self.__data_arrived(body)

    def __data_arrived(self, body):
        header, filtered_trips = decode(body)

        for trip in filtered_trips:
            trip = trip.split(",")
            key, value = self.gen_key_value(trip)
            self.groupby.add_data(key, value)

    def __eof_arrived(self):
        self.__send_to_apply()
        self.em_queue.send(ack_msg())
        print("action: eof_trips_arrived")

    def __send_to_apply(self):
        grouped_data = []

        for key in self.groupby.grouped_data:
            value = self.groupby.grouped_data[key]
            grouped_data.append(self.__str_from_key_value(key, value))
            # msg = construct_msg([self.__str_from_key_value(key, value)])
            # self.send_queue.send(msg)
        msg = construct_msg(grouped_data)
        self.send_queue.send(msg)

    def __str_from_key_value(self, key, value):
        to_ret = f"{key},"
        for v in value:
            to_ret += f"{v},"

        return to_ret[: len(to_ret) - 1]

    def stop(self, *args):
        if self.running:
            self.queue_connection.stop_receiving()
            self.queue_connection.close()
            print(
                "action: close_resource | result: success | resource: rabbit_connection"
            )

            self.running = False

        sys.exit(0)
