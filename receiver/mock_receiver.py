from common.connection import Connection
from data.data import stations, weathers, trips
import time

def main():
    S_QUEUE = "stations_queue"
    JOIN_TRIPS_STATIONS_QUEUE = "join_trip_station_queue"
    TRIPS_QUEUE = "trips_queue"

    #W_QUEUE = "weather_queue"

    conn = Connection()

    s_q = conn.basic_queue(S_QUEUE)
    #w_q = conn.basic_queue(W_QUEUE)

    s_q.send('REGISTER_EOF')

    """
    for msg in weathers:
        w_q.send(bytes(msg, 'utf-8'))
    w_q.send(b'last')"""

    # debería ser de workers:
    send_trips_queues = [conn.basic_queue(TRIPS_QUEUE), conn.basic_queue(JOIN_TRIPS_STATIONS_QUEUE)]
    for queue in send_trips_queues:
            queue.send('REGISTER_EOF')

    time.sleep(3)

    for msg in stations:
        s_q.send(bytes(msg, 'utf-8'))
    s_q.send(b'last')

    for trip in trips:
        for queue in send_trips_queues:
            queue.send(bytes(trip, 'utf-8'))

    for queue in send_trips_queues:
        queue.send('EOF')

    s_q.send('EOF')

    conn.close()