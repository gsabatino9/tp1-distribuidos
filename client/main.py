import time, os, logging
from client import Client
from common.utils import initialize_log, initialize_config

HOST = os.environ['HOST']
PORT_STATIC = int(os.environ['PORT_STATIC'])
PORT_TRIPS = int(os.environ['PORT_TRIPS'])

def main():
	initialize_log()
	client = Client(HOST, PORT_STATIC, PORT_TRIPS)
	logging.info(f"action: client_up | result: success |	Host: {HOST} | Ports: {PORT_STATIC},{PORT_TRIPS}")
	
	client.run()

if __name__ == "__main__":
	time.sleep(11)
	main()