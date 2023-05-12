FROM python:3.9.7-slim
RUN pip install --upgrade pip && pip3 install pika

COPY server/eof_manager/groupby /
COPY server/queue /server/queue
COPY protocol /protocol
COPY server/eof_manager/common /server/eof_manager/common

ENTRYPOINT ["/bin/sh"]
