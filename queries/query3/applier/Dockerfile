FROM python:3.9.7-slim
RUN pip install --upgrade pip && pip3 install pika

COPY /queries/query3/applier /
COPY common /common

ENTRYPOINT ["/bin/sh"]
