FROM python:3.9.7-slim
RUN pip install --upgrade pip && pip3 install pika

COPY joiners/weather_handler /
COPY common /common

ENTRYPOINT ["/bin/sh"]
