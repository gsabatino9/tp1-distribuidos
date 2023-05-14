from groupby_query2 import GroupbyQuery2
import os

NAME_RECV_QUEUE = os.environ.get("NAME_RECV_QUEUE")
NAME_EM_QUEUE = os.environ.get("NAME_EM_QUEUE")
NAME_SEND_QUEUE = os.environ.get("NAME_SEND_QUEUE")


def main():
    g = GroupbyQuery2(NAME_RECV_QUEUE, NAME_EM_QUEUE, NAME_SEND_QUEUE)
    g.stop()


if __name__ == "__main__":
    main()
