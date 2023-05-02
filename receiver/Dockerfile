FROM python:3.9.7-slim
RUN pip install --upgrade pip && pip3 install pika

COPY receiver /
COPY common /common
COPY data /data
COPY protocol /protocol

ENTRYPOINT ["/bin/sh"]
