FROM python:3.9.7-slim
RUN pip install --upgrade pip && pip3 install pika

COPY /query3/groupby /
COPY common /common
RUN pip install haversine

ENTRYPOINT ["/bin/sh"]
