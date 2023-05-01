FROM python:3.9.7-slim
RUN pip install --upgrade pip && pip3 install pika

COPY eof_manager/filter /
COPY common /common
COPY eof_manager /eof_manager

ENTRYPOINT ["/bin/sh"]
