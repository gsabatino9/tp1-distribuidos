from common.connection import Connection
from data.data import stations, weathers, trips
import time

def main():
    S_QUEUE = "stations_queue"
    JOIN_TRIPS_STATIONS_QUEUE = "join_trip_station_queue"
    TRIPS_QUEUE = "trips_queue"
    EM_QUEUE = "eof_handler_queue"

    #W_QUEUE = "weather_queue"

    conn = Connection()

    s_q = conn.basic_queue(S_QUEUE)
    #w_q = conn.basic_queue(W_QUEUE)

    for msg in stations:
        s_q.send(bytes(msg, 'utf-8'))
    s_q.send(b'last')

    """
    for msg in weathers:
        w_q.send(bytes(msg, 'utf-8'))
    w_q.send(b'last')"""

    # debería ser de workers:
    send_trips_queues = [conn.basic_queue(TRIPS_QUEUE), conn.basic_queue(JOIN_TRIPS_STATIONS_QUEUE)]
    first_em_queue = conn.pubsub_queue(EM_QUEUE)

    time.sleep(3)

    for trip in trips:
        for queue in send_trips_queues:
            queue.send(bytes(trip, 'utf-8'))

    first_em_queue.send('EOF')

    conn.close()