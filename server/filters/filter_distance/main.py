from filter_distance import FilterDistance

NAME_RECV_EXCHANGE = "filter_joined_stations_q"
NAME_RECV_QUEUE = "filter_distance_q"
NAME_EM_QUEUE = "eof_manager_filters_q"
NAME_SEND_QUEUE = "groupby_query3_q"


def main():
    f = FilterDistance(
        NAME_RECV_EXCHANGE, NAME_RECV_QUEUE, NAME_EM_QUEUE, NAME_SEND_QUEUE
    )
    f.stop()


if __name__ == "__main__":
    main()
