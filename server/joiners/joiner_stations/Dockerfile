FROM python:3.9.7-slim
RUN pip install --upgrade pip && pip3 install pika

COPY server/joiners/joiner_stations /
COPY server/queue /server/queue
COPY protocol /protocol
COPY server/eof_manager /server/eof_manager
COPY server/common /server/common

ENTRYPOINT ["/bin/sh"]
