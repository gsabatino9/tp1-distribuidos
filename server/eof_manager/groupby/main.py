from eof_manager import EOFManager
import os

NAME_RECV_QUEUE = 'eof_manager_groupby_q'
NAME_GROUPBY_QUEUE = ['groupby_query1_q']

def main():
	e = EOFManager(NAME_RECV_QUEUE, NAME_GROUPBY_QUEUE)
	e.stop()

if __name__ == "__main__":
	main()