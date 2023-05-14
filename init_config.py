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
  <FILTER_DISTANCE>

  <GROUPBY_QUERY1>
  <GROUPBY_QUERY2>
  <GROUPBY_QUERY3>

  <APPLIER_QUERY1>
  <APPLIER_QUERY2>
  <APPLIER_QUERY3>

  <RESULTS_VERIFIER>

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
  <EM_RESULTS>

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

FILTER_DISTANCE = """
  filter_distance_{}:
    container_name: filter_distance_{}
    entrypoint: python3 /main.py
    environment:
      - PYTHONUNBUFFERED=1
    image: filter_distance:latest
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

GROUPBY_QUERY3 = """
  groupby_query3:
    container_name: groupby_query3
    entrypoint: python3 /main.py
    environment:
      - PYTHONUNBUFFERED=1
    image: groupby_query3:latest
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

APPLIER_QUERY3 = """
  applier_query3_{}:
    container_name: applier_query3_{}
    entrypoint: python3 /main.py
    environment:
      - PYTHONUNBUFFERED=1
    image: applier_query3:latest
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

EM_RESULTS = """
  eof_manager_query_results:
    container_name: eof_manager_query_results
    entrypoint: python3 /main.py
    environment:
      - PYTHONUNBUFFERED=1
    image: eof_manager_query_results:latest
    networks:      
      - testing_net
    depends_on:
      rabbitmq:
        condition: service_healthy
"""

RESULTS_VERIFIER = """
  results_verifier:
    container_name: results_verifier
    entrypoint: python3 /main.py
    environment:
      - PYTHONUNBUFFERED=1
    ports:
      - 12346:12346
    image: results_verifier:latest
    networks:      
      - testing_net
    depends_on:
      rabbitmq:
        condition: service_healthy
"""