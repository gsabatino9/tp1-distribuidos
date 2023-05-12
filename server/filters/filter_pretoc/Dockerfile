FROM python:3.9.7-slim
RUN pip install --upgrade pip && pip3 install pika

COPY server/filters/filter_pretoc /
COPY server/queue /server/queue
COPY server/filters/common /server/filters/common
COPY protocol /protocol

ENTRYPOINT ["/bin/sh"]
