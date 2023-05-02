import time, os
from client import Client

HOST = os.environ['HOST']
PORT_STATIC = int(os.environ['PORT_STATIC'])
PORT_TRIPS = int(os.environ['PORT_TRIPS'])

def main():
	client = Client(HOST, PORT_STATIC, PORT_TRIPS)	
	client.run()

if __name__ == "__main__":
	time.sleep(11)
	main()