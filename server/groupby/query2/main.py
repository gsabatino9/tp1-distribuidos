from groupby_query2 import GroupbyQuery2
import os

NAME_RECV_QUEUE = "groupby_query2_q"
NAME_EM_QUEUE = "eof_manager_groupby_q"
NAME_SEND_QUEUE = "applier_query2_q"


def main():
    g = GroupbyQuery2(NAME_RECV_QUEUE, NAME_EM_QUEUE, NAME_SEND_QUEUE)
    g.stop()


if __name__ == "__main__":
    main()
