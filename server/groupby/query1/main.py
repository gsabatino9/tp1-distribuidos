from groupby_query1 import GroupbyQuery1
import os

NAME_RECV_QUEUE = "groupby_query1_q"
NAME_EM_QUEUE = "eof_manager_groupby_q"
NAME_SEND_QUEUE = "applier_query1_q"


def main():
    g = GroupbyQuery1(NAME_RECV_QUEUE, NAME_EM_QUEUE, NAME_SEND_QUEUE)
    g.stop()


if __name__ == "__main__":
    main()
