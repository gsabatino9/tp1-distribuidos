import signal, sys
from server.common.queue.connection import Connection
from server.common.utils_messages_eof import *


class EOFManager:
    def __init__(
        self, name_recv_queue, name_filters_queue, name_send_queue, size_workers
    ):
        self.__init_eof_manager(size_workers)

        self.__connect(name_recv_queue, name_filters_queue, name_send_queue)

    def __init_eof_manager(self, size_workers):
        self.running = True
        signal.signal(signal.SIGTERM, self.stop)

        self.size_workers = size_workers
        self.sum_workers = sum(size_workers)
        self.acks = 0

    def __connect(self, name_recv_queue, name_filters_queue, name_send_queue):
        # try-except
        self.queue_connection = Connection()

        self.recv_queue = self.queue_connection.pubsub_queue(name_recv_queue)
        self.recv_queue.receive(self.receive_msg)

        self.filters_queues = [
            self.queue_connection.basic_queue(q) for q in name_filters_queue
        ]
        self.send_queue = self.queue_connection.pubsub_queue(name_send_queue)

        self.queue_connection.start_receiving()

    def receive_msg(self, ch, method, properties, body):
        header = decode(body)

        if is_eof(header):
            self.__send_eofs(header, body)
        else:
            self.__recv_ack_trips(header, body)

    def __send_eofs(self, header, msg):
        for i, size_w in enumerate(self.size_workers):
            for _ in range(size_w):
                self.filters_queues[i].send(msg)

    def __recv_ack_trips(self, header, body):
        self.acks += 1

        if self.acks == self.sum_workers:
            print("EOF trips ackeados.")
            self.send_queue.send(eof_msg(header))

    def stop(self, *args):
        if self.running:
            self.queue_connection.stop_receiving()
            self.queue_connection.close()

            self.running = False
            print("EOFManagerFilters cerrado correctamente.")

        sys.exit(0)
