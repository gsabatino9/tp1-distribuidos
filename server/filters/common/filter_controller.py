import signal, sys
from server.common.queue.connection import Connection
from server.filters.common.filter import Filter
from server.common.utils_messages_client import decode, is_eof, construct_msg
from server.common.utils_messages_eof import ack_msg


class FilterController:
    def __init__(
        self,
        name_recv_exchange,
        name_recv_queue,
        name_em_queue,
        name_send_queue,
        columns_names,
        reduced_columns,
        func_filter,
    ):
        self.__init_filter(columns_names, reduced_columns, func_filter)

        self.__connect(
            name_recv_exchange, name_recv_queue, name_em_queue, name_send_queue
        )
        self.recv_queue.receive(self.proccess_message)
        self.queue_connection.start_receiving()

    def __init_filter(self, columns_names, reduced_columns, func_filter):
        self.running = True
        signal.signal(signal.SIGTERM, self.stop)

        self.not_filtered = 0
        self.filter = Filter(columns_names, reduced_columns, func_filter)

        print("action: filter_started | result: success")

    def __connect(
        self, name_recv_exchange, name_recv_queue, name_em_queue, name_send_queue
    ):
        self.queue_connection = Connection()
        self.recv_queue = self.queue_connection.pubsub_worker_queue(
            name_recv_exchange, name_recv_queue
        )
        self.em_queue = self.queue_connection.pubsub_queue(name_em_queue)
        self.send_queue = self.queue_connection.basic_queue(name_send_queue)

    def proccess_message(self, ch, method, properties, body):
        if is_eof(body):
            self.__eof_arrived(ch)
        else:
            self.__filter(body)

    def __filter(self, body):
        header, joined_trips = decode(body)
        trips_to_next_stage = []

        for trip in joined_trips:
            new_trip = self.filter.apply(trip)
            if new_trip:
                self.not_filtered += 1
                trips_to_next_stage.append(new_trip)

        self.__send_next_stage(header, trips_to_next_stage)

    def __send_next_stage(self, header, trips_to_next_stage):
        if len(trips_to_next_stage) > 0:
            msg = construct_msg(header, trips_to_next_stage)
            self.send_queue.send(msg)

    def __eof_arrived(self, ch):
        ch.stop_consuming()
        self.em_queue.send(ack_msg())
        print(f"action: eof_trips_arrived | not_filtered_trips: {self.not_filtered}")

    def stop(self, *args):
        if self.running:
            self.queue_connection.stop_receiving()
            self.queue_connection.close()
            print(
                "action: close_resource | result: success | resource: rabbit_connection"
            )

            self.running = False

        sys.exit(0)
