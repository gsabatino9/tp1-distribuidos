FROM python:3.9.7-slim
RUN pip install --upgrade pip && pip3 install pika

COPY server/receiver /
COPY protocol /protocol
COPY server/queue /server/queue
COPY server/eof_manager /server/eof_manager
COPY server/common /server/common

ENTRYPOINT ["/bin/sh"]
