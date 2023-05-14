import signal, sys
from server.common.queue.connection import Connection
from server.common.utils_messages_client import *
from server.common.utils_messages_eof import ack_msg


class JoinerController:
    def __init__(
        self,
        name_recv_queue,
        name_trips_queue,
        name_em_queue,
        name_next_stage_queue,
        joiner,
    ):
        self.__init_joiner(joiner)

        self.__connect(
            name_recv_queue, name_trips_queue, name_em_queue, name_next_stage_queue
        )

    def __init_joiner(self, joiner):
        self.running = True
        signal.signal(signal.SIGTERM, self.stop)

        self.joiner = joiner

    def __connect(
        self, name_recv_queue, name_trips_queue, name_em_queue, name_next_stage_queue
    ):
        self.queue_connection = Connection()
        self.recv_queue = self.queue_connection.basic_queue(name_recv_queue)
        self.trips_queue = self.queue_connection.basic_queue(name_trips_queue)
        self.em_queue = self.queue_connection.pubsub_queue(name_em_queue)
        self.next_stage_queue = self.queue_connection.pubsub_queue(
            name_next_stage_queue
        )

        self.recv_queue.receive(self.process_messages)
        self.queue_connection.start_receiving()

    def process_messages(self, ch, method, properties, body):
        if is_eof(body):
            self.__last_static_data_arrived()
        else:
            self.__static_data_arrived(body)

    def __last_static_data_arrived(self):
        print(f"Todas los datos estáticos llegaron llegaron")
        self.amount_joined = 0
        self.trips_queue.receive(self.process_join_messages)

    def __static_data_arrived(self, body):
        header, chunk_data = decode(body)
        city = obtain_city(header)

        for data in chunk_data:
            data = data.split(",")
            self.joiner.add_data(city, data)

    def process_join_messages(self, ch, method, properties, body):
        if is_eof(body):
            self.__last_trip_arrived()
        else:
            self.__request_join_arrived(body)

    def __request_join_arrived(self, body):
        header, trips = decode(body)
        city = obtain_city(header)
        joined_trips = []

        for trip in trips:
            trip = trip.split(",")
            ret = self.joiner.join_trip(city, trip)
            if ret:
                self.amount_joined += 1
                joined_trips.append(ret)

        self.__send_next_stage(header, joined_trips)

    def __send_next_stage(self, header, joined_trips):
        if len(joined_trips) > 0:
            msg = construct_msg(header, joined_trips)
            self.next_stage_queue.send(msg)

    def __last_trip_arrived(self):
        self.em_queue.send(ack_msg())
        print(f"EOF trips - Joined: {self.amount_joined}")

    def stop(self, *args):
        if self.running:
            self.queue_connection.stop_receiving()
            self.queue_connection.close()

            self.running = False
            print("Joiner cerrado correctamente.")

        sys.exit(0)
