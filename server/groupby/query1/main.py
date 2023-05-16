from groupby_query1 import GroupbyQuery1
import os

NAME_RECV_QUEUE = os.environ.get("NAME_RECV_QUEUE")
NAME_EM_QUEUE = os.environ.get("NAME_EM_QUEUE")
NAME_SEND_QUEUE = os.environ.get("NAME_SEND_QUEUE")
CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE"))


def main():
    g = GroupbyQuery1(NAME_RECV_QUEUE, NAME_EM_QUEUE, NAME_SEND_QUEUE, CHUNK_SIZE)
    g.stop()


if __name__ == "__main__":
    main()
