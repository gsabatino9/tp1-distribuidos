FROM python:3.9.7-slim
RUN pip install --upgrade pip && pip3 install pika

COPY server/joiners/joiner_weather /
COPY server/queue /server/queue
COPY protocol /protocol
COPY server/eof_manager /server/eof_manager

ENTRYPOINT ["/bin/sh"]
