FROM python:3.9.7-slim
RUN pip install --upgrade pip && pip3 install pika

COPY /query2/applier /
COPY common /common

ENTRYPOINT ["/bin/sh"]
