import socket, signal, sys
from protocol.communication_server import CommunicationServer
from server.common.queue.connection import Connection
from server.common.utils_messages_eof import ack_msg
from server.common.utils_messages_group import decode, is_eof


class ResultsVerifier:
    def __init__(self, name_recv_queue, name_em_queue, host, port):
        self.__init_results_verifier(host, port)

        self.__connect(name_recv_queue, name_em_queue)
        self.recv_queue.receive(self.process_messages)
        self.queue_connection.start_receiving()

    def __init_results_verifier(self, host, port):
        self.running = True
        signal.signal(signal.SIGTERM, self.stop)

        self.queries_results = {i: [] for i in range(1, 4)}
        self.queries_ended = {i: False for i in range(1, 4)}
        self.addr = (host, port)

        print("action: results_verifier_started | result: success")

    def __connect(self, name_recv_queue, name_em_queue):
        self.queue_connection = Connection()
        self.recv_queue = self.queue_connection.routing_queue(
            name_recv_queue, routing_keys=["1", "2", "3"]
        )
        self.em_queue = self.queue_connection.pubsub_queue(name_em_queue)

    def process_messages(self, ch, method, properties, body):
        id_query = int(method.routing_key)
        if is_eof(body):
            print("action: eof_trips_arrived")
            self.__eof_arrived(id_query)
        else:
            self.__query_result_arrived(body, id_query)

    def __query_result_arrived(self, body, id_query):
        header, results = decode(body)
        self.queries_results[id_query] += results

    def __eof_arrived(self, id_query):
        self.em_queue.send(ack_msg())
        self.queries_ended[id_query] = True

        self.__verify_last_result()

    def __verify_last_result(self):
        ended = True
        for query in self.queries_ended:
            if not self.queries_ended[query]:
                ended = False

        if ended:
            print(
                f"action: results_ready | result: success | results: {self.queries_results}"
            )
            self.__inform_results()

    def __inform_results(self):
        self.__connect_with_client()
        self.__send_results()

    def __connect_with_client(self):
        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        skt.bind(self.addr)
        skt.listen()

        client_socket, _ = skt.accept()
        self.client_connection = CommunicationServer(client_socket)
        print(
            "action: client_connected | result: success | msg: starting to send results"
        )

    def __send_results(self):
        for query in self.queries_results:
            results = self.queries_results[query]
            if len(results) > 0:
                self.client_connection.send_results(query, results)

        self.client_connection.send_last()
        print("action: results_sent | result: success")

    def stop(self, *args):
        if self.running:
            self.queue_connection.stop_receiving()
            self.queue_connection.close()
            print(
                "action: close_resource | result: success | resource: rabbit_connection"
            )
            if hasattr(self, "client_connection"):
                self.client_connection.stop()
                print(
                    "action: close_resource | result: success | resource: client_connection"
                )

            self.running = False

        sys.exit(0)
