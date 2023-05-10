FROM python:3.9.7-slim
RUN pip install --upgrade pip && pip3 install pika

COPY server/eof_manager /
COPY server/queue /server/queue
COPY protocol /protocol

ENTRYPOINT ["/bin/sh"]
