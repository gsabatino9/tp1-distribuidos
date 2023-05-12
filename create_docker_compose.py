import sys

INIT_DOCKER = """version: '3'
services:
  rabbitmq:
    image: rabbitmq:3-management-alpine
    container_name: rabbitmq
    ports:
      - 15672:15672
      - 5672:5672
    networks:      
      - testing_net
    healthcheck:        
      test: [ "CMD", "nc", "-z", "localhost", "5672" ]
      interval: 10s        
      timeout: 5s        
      retries: 10
    logging:
      driver: none

  <RECEIVER>

  <JOINER_STATIONS>
  <JOINER_WEATHER>

  <FILTER_PRETOC>
  <FILTER_YEAR>

  <GROUPBY_QUERY1>
  <GROUPBY_QUERY2>

  <APPLIER_QUERY1>
  <APPLIER_QUERY2>

  eof_manager_joiners:
    container_name: eof_manager_joiners
    entrypoint: python3 /main.py
    environment:
      - PYTHONUNBUFFERED=1
    image: eof_manager_joiners:latest
    networks:      
      - testing_net
    depends_on:
      rabbitmq:
        condition: service_healthy
    
  <EM_FILTERS>
  <EM_GROUPBY>
  <EM_APPLIERS>

networks:
  testing_net:
    driver: bridge
"""

RECEIVER = """
  receiver:
    container_name: receiver
    entrypoint: python3 /main.py
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=receiver
      - PORT=12345
      - NAME_STATIONS_QUEUE={}
      - NAME_WEATHER_QUEUE={}
      - NAME_TRIPS_QUEUES={}
      - NAME_EM_QUEUE={}
    image: receiver:latest
    ports:
      - 12345:12345
      - 12346:12346
    networks:      
      - testing_net
    depends_on:
      rabbitmq:
        condition: service_healthy
"""

JOINER_STATIONS = """
  joiner_stations:
    container_name: joiner_stations
    entrypoint: python3 /main.py
    environment:
      - PYTHONUNBUFFERED=1
      - NAME_RECV_QUEUE={}
      - NAME_TRIPS_QUEUE={}
      - NAME_EM_QUEUE={}
      - NAME_NEXT_STAGE_QUEUE={}
    image: joiner_stations:latest
    networks:      
      - testing_net
    depends_on:
      rabbitmq:
        condition: service_healthy
"""

JOINER_WEATHER = """
  joiner_weather:
    container_name: joiner_weather
    entrypoint: python3 /main.py
    environment:
      - PYTHONUNBUFFERED=1
      - NAME_RECV_QUEUE={}
      - NAME_TRIPS_QUEUE={}
      - NAME_EM_QUEUE={}
      - NAME_NEXT_STAGE_QUEUE={}
    image: joiner_weather:latest
    networks:      
      - testing_net
    depends_on:
      rabbitmq:
        condition: service_healthy
"""

FILTER_PRETOC = """
  filter_pretoc_{}:
    container_name: filter_pretoc_{}
    entrypoint: python3 /main.py
    environment:
      - PYTHONUNBUFFERED=1
    image: filter_pretoc:latest
    networks:      
      - testing_net
    depends_on:
      rabbitmq:
        condition: service_healthy
"""

FILTER_YEAR = """
  filter_year_{}:
    container_name: filter_year_{}
    entrypoint: python3 /main.py
    environment:
      - PYTHONUNBUFFERED=1
    image: filter_year:latest
    networks:      
      - testing_net
    depends_on:
      rabbitmq:
        condition: service_healthy
"""

EM_FILTERS = """
  eof_manager_filters:
    container_name: eof_manager_filters
    entrypoint: python3 /main.py
    environment:
      - PYTHONUNBUFFERED=1
      - SIZE_WORKERS={}
    image: eof_manager_filters:latest
    networks:      
      - testing_net
    depends_on:
      rabbitmq:
        condition: service_healthy
"""

GROUPBY_QUERY1 = """
  groupby_query1:
    container_name: groupby_query1
    entrypoint: python3 /main.py
    environment:
      - PYTHONUNBUFFERED=1
    image: groupby_query1:latest
    networks:      
      - testing_net
    depends_on:
      rabbitmq:
        condition: service_healthy
"""

GROUPBY_QUERY2 = """
  groupby_query2:
    container_name: groupby_query2
    entrypoint: python3 /main.py
    environment:
      - PYTHONUNBUFFERED=1
    image: groupby_query2:latest
    networks:      
      - testing_net
    depends_on:
      rabbitmq:
        condition: service_healthy
"""

APPLIER_QUERY1 = """
  applier_query1_{}:
    container_name: applier_query1_{}
    entrypoint: python3 /main.py
    environment:
      - PYTHONUNBUFFERED=1
    image: applier_query1:latest
    networks:      
      - testing_net
    depends_on:
      rabbitmq:
        condition: service_healthy
"""

APPLIER_QUERY2 = """
  applier_query2_{}:
    container_name: applier_query2_{}
    entrypoint: python3 /main.py
    environment:
      - PYTHONUNBUFFERED=1
    image: applier_query2:latest
    networks:      
      - testing_net
    depends_on:
      rabbitmq:
        condition: service_healthy
"""

EM_GROUPBY = """
  eof_manager_groupby:
    container_name: eof_manager_groupby
    entrypoint: python3 /main.py
    environment:
      - PYTHONUNBUFFERED=1
    image: eof_manager_groupby:latest
    networks:      
      - testing_net
    depends_on:
      rabbitmq:
        condition: service_healthy
"""

EM_APPLIERS = """
  eof_manager_applier:
    container_name: eof_manager_applier
    entrypoint: python3 /main.py
    environment:
      - PYTHONUNBUFFERED=1
      - SIZE_WORKERS={}
    image: eof_manager_applier:latest
    networks:      
      - testing_net
    depends_on:
      rabbitmq:
        condition: service_healthy
"""

NAME_STATIONS_QUEUE = 'joiner_stations_q'
NAME_WEATHER_QUEUE = 'joiner_weather_q'
NAME_TRIPS_QUEUES = ['join_trip_weather_q', 'join_trip_stations_q']
NAME_EM_JOINERS_QUEUE = 'eof_manager_joiners_q'
NAME_FILTER_STATIONS_QUEUE = 'filter_joined_stations_q'
NAME_FILTER_WEATHER_QUEUE = 'filter_joined_weather_q'

def main():
    num_filters_pretoc = int(sys.argv[1])
    num_filters_year = int(sys.argv[2])
    num_appliers_query1 = int(sys.argv[3])
    num_appliers_query2 = int(sys.argv[4])

    receiver = RECEIVER.format(NAME_STATIONS_QUEUE, NAME_WEATHER_QUEUE, NAME_TRIPS_QUEUES, NAME_EM_JOINERS_QUEUE)
    joiner_stations = JOINER_STATIONS.format(NAME_STATIONS_QUEUE, NAME_TRIPS_QUEUES[1], NAME_EM_JOINERS_QUEUE, NAME_FILTER_STATIONS_QUEUE)
    joiner_weather = JOINER_WEATHER.format(NAME_WEATHER_QUEUE, NAME_TRIPS_QUEUES[0], NAME_EM_JOINERS_QUEUE, NAME_FILTER_WEATHER_QUEUE)

    filters_pretoc = ""
    for i in range(1,num_filters_pretoc+1):
        filters_pretoc += FILTER_PRETOC.format(i, i)

    filters_year = ""
    for i in range(1,num_filters_year+1):
        filters_year += FILTER_YEAR.format(i, i)

    em_filters = EM_FILTERS.format([num_filters_pretoc, num_filters_year])
    
    appliers_query1 = ""
    for i in range(1,num_appliers_query1+1):
        appliers_query1 += APPLIER_QUERY1.format(i, i)

    appliers_query2 = ""
    for i in range(1,num_appliers_query2+1):
        appliers_query2 += APPLIER_QUERY2.format(i, i)

    em_appliers = EM_APPLIERS.format([num_appliers_query1, num_appliers_query2])

    compose = INIT_DOCKER.format() \
                  .replace("<RECEIVER>", receiver) \
                  .replace("<JOINER_STATIONS>", joiner_stations) \
                  .replace("<JOINER_WEATHER>", joiner_weather) \
                  .replace("<FILTER_PRETOC>", filters_pretoc) \
                  .replace("<FILTER_YEAR>", filters_year) \
                  .replace("<EM_FILTERS>", em_filters) \
                  .replace("<EM_GROUPBY>", EM_GROUPBY) \
                  .replace("<GROUPBY_QUERY1>", GROUPBY_QUERY1) \
                  .replace("<GROUPBY_QUERY2>", GROUPBY_QUERY2) \
                  .replace("<APPLIER_QUERY1>", appliers_query1) \
                  .replace("<APPLIER_QUERY2>", appliers_query2) \
                  .replace("<EM_APPLIERS>", em_appliers)
    
    with open("docker-compose-server.yaml", "w") as compose_file:
        compose_file.write(compose)

if __name__ == "__main__":
    main()