import signal, sys
from server.common.queue.connection import Connection
from server.applier.common.applier import Applier
from server.common.utils_messages_eof import ack_msg
from server.common.utils_messages_group import decode, is_eof, construct_msg


class ApplierController:
    def __init__(
        self,
        name_recv_queue,
        name_em_queue,
        name_send_queue,
        id_query,
        operation,
        gen_result_msg,
    ):
        self.__init_applier(str(id_query), gen_result_msg, operation)

        self.__connect(name_recv_queue, name_em_queue, name_send_queue)
        self.recv_queue.receive(self.process_messages)
        self.queue_connection.start_receiving()

    def __init_applier(self, id_query, gen_result_msg, operation):
        self.running = True
        signal.signal(signal.SIGTERM, self.stop)

        self.id_query = id_query
        self.gen_result_msg = gen_result_msg
        self.applier = Applier(operation)

        print("action: applier_started | result: success")

    def __connect(self, name_recv_queue, name_em_queue, name_send_queue):
        self.queue_connection = Connection()
        self.recv_queue = self.queue_connection.basic_queue(name_recv_queue)
        self.send_queue = self.queue_connection.routing_queue(name_send_queue)

        self.em_queue = self.queue_connection.pubsub_queue(name_em_queue)

    def process_messages(self, ch, method, properties, body):
        if is_eof(body):
            self.__eof_arrived(ch)
        else:
            self.__apply(body)

    def __apply(self, body):
        header, agrouped_trips = decode(body)
        result_trips = []

        for trip in agrouped_trips:
            trip = trip.split(",")
            try:
                result, msg_to_send = self.gen_result_msg(trip, self.applier)
                if result:
                    result_trips.append(msg_to_send)
            except:
                print("action: ignore_trip | msg: invalid or empty trip arrived")

        self.__send_result(result_trips)

    def __send_result(self, trips_to_next_stage):
        if len(trips_to_next_stage) > 0:
            msg = construct_msg(trips_to_next_stage)
            self.send_queue.send(msg, routing_key=self.id_query)

    def __eof_arrived(self, ch):
        ch.stop_consuming()
        self.em_queue.send(ack_msg())
        print("action: eof_trips_arrived")

    def stop(self, *args):
        if self.running:
            self.queue_connection.stop_receiving()
            self.queue_connection.close()
            print(
                "action: close_resource | result: success | resource: rabbit_connection"
            )

            self.running = False

        sys.exit(0)
