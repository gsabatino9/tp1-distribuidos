from receiver import Receiver
import os

HOST = 'receiver'
PORT = 12345
NEXT_QUEUE = 'data_router_q'
NAME_EM_QUEUE = 'eof_manager_q'
SIZE_WORKERS = int(os.environ.get('SIZE_WORKERS'))

def main():
	receiver = Receiver(HOST, PORT, NEXT_QUEUE, NAME_EM_QUEUE, SIZE_WORKERS)
	receiver.run()
	receiver.stop()

if __name__ == "__main__":
	main()