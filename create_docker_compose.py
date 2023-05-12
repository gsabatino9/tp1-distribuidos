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

  receiver:
    container_name: receiver
    entrypoint: python3 /main.py
    environment:
      - PYTHONUNBUFFERED=1
    image: receiver:latest
    ports:
      - 12345:12345
      - 12346:12346
    networks:      
      - testing_net
    depends_on:
      rabbitmq:
        condition: service_healthy

  <JOINER_STATIONS>
  <JOINER_WEATHER>

  <FILTER_PRETOC>
  <FILTER_YEAR>

  <GROUPBY_QUERY1>

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

networks:
  testing_net:
    driver: bridge
"""

JOINER_STATIONS = """
  joiner_stations:
    container_name: joiner_stations
    entrypoint: python3 /main.py
    environment:
      - PYTHONUNBUFFERED=1
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


def main():
    num_filters_pretoc = int(sys.argv[1])
    num_filters_year = int(sys.argv[2])

    filters_pretoc = ""
    for i in range(1,num_filters_pretoc+1):
        filters_pretoc += FILTER_PRETOC.format(i, i)

    filters_year = ""
    for i in range(1,num_filters_year+1):
        filters_year += FILTER_YEAR.format(i, i)

    em_filters = EM_FILTERS.format([num_filters_pretoc, num_filters_year])

    compose = INIT_DOCKER.format() \
                  .replace("<JOINER_STATIONS>", JOINER_STATIONS) \
                  .replace("<JOINER_WEATHER>", JOINER_WEATHER) \
                  .replace("<FILTER_PRETOC>", filters_pretoc) \
                  .replace("<FILTER_YEAR>", filters_year) \
                  .replace("<EM_FILTERS>", em_filters) \
                  .replace("<EM_GROUPBY>", EM_GROUPBY) \
                  .replace("<GROUPBY_QUERY1>", GROUPBY_QUERY1)
    
    with open("docker-compose-server.yaml", "w") as compose_file:
        compose_file.write(compose)

if __name__ == "__main__":
    main()