from protocol.communication_client import CommunicationClient
from utils import construct_payload, construct_city, is_eof
import csv, socket, threading, time, signal, sys
from itertools import islice
from datetime import datetime, timedelta


class Client:
    def __init__(self, host, port, chunk_size):
        self.__init_client(chunk_size)

        # try-except
        skt = self.__connect(host, port)
        self.conn = CommunicationClient(skt)
        print(
            f"action: client_connected | result: success | addr: {self.conn.getpeername()}"
        )

    def __init_client(self, chunk_size):
        self.running = True
        signal.signal(signal.SIGTERM, self.stop)

        self.chunk_size = chunk_size

    def __connect(self, host, port):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        return client_socket

    def run(self, filepaths, types_files, cities, addr_consult):
        self.__send_files(filepaths, types_files, cities)
        self.__get_results(addr_consult)

    def __send_files(self, filepaths, types_files, cities):
        threads = []

        for file in types_files:
            self.__send_type_file(filepaths, file, cities)

        print(f"action: waiting_ack_files")
        self.conn.recv_files_received()
        print(f"action: ack_files | result: success | msg: all files sent to server")
        self.conn.stop()

    # manda todo de una stations, weather o trips
    def __send_type_file(self, filepaths, type_file, cities):
        send_data = 0
        for i, filepath in enumerate(filepaths):
            with open(filepath + type_file + ".csv", newline="") as csvfile:
                reader = csv.reader(csvfile, delimiter=",")

                # skip header
                next(reader)
                last_chunk = False
                while True:
                    chunk = list(islice(reader, self.chunk_size))
                    if not chunk:
                        break
                    chunk = self.__preprocess_chunk(type_file, chunk)
                    self.__send_chunk(type_file, chunk, cities[i], False)
                    send_data += 1

        self.__send_chunk(type_file, list(""), cities[i], True)
        print(
            f"action: file_sent | result: success | type_file: {type_file} | amount_chunks: {send_data}"
        )

    def __send_chunk(self, data_type, chunk, city, last_chunk):
        city = construct_city(city)
        payload = construct_payload(chunk)
        self.conn.send(data_type, payload, city, last_chunk)

    def __preprocess_chunk(self, type_file, chunk):
        if type_file == "trips":
            for row in chunk:
                start_date = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                end_date = datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S")
                row[0] = start_date.strftime("%Y-%m-%d")
                row[2] = end_date.strftime("%Y-%m-%d")
        elif type_file == "weather":
            for row in chunk:
                fecha_dt = datetime.strptime(row[0], "%Y-%m-%d")
                nueva_fecha = fecha_dt - timedelta(days=1)
                row[0] = nueva_fecha.strftime("%Y-%m-%d")

        return chunk

    def __get_results(self, addr_consult):
        self.__connect_with_consults_server(addr_consult[0], addr_consult[1])
        results = {i: [] for i in range(1, 4)}
        ended = False

        while not ended:
            header, payload = self.conn.recv_results()
            if is_eof(header):
                ended = True
                print(f"action: results_obtained | result: success")
            else:
                results[header.id_query].append(payload.data)

        print(results)
        self.__save_results(results)

    def __save_results(self, results):
        with open("results/output.csv", "w", newline="") as f:
            writer = csv.writer(f)
            for key, values in results.items():
                for row in values:
                    for value in row:
                        writer.writerow([key] + [value])

    def __connect_with_consults_server(self, host, port):
        connected = False
        while not connected:
            try:
                skt = self.__connect(host, port)
                self.conn = CommunicationClient(skt)
                print(
                    f"action: client_connected | result: success | addr: {self.conn.getpeername()}"
                )
                connected = True
            except:
                print(
                    f"action: client_connected | result: failure | msg: retry in 1 sec"
                )
                time.sleep(1)

    def stop(self, *args):
        if self.running:
            if hasattr(self, "conn"):
                self.conn.stop()
                print("action: close_resource | result: success | resource: connection")

            self.running = False
            print("Client cerrado correctamente.")

        sys.exit(0)
