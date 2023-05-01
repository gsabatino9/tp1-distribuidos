FROM python:3.9.7-slim
RUN pip install --upgrade pip && pip3 install pika

COPY eof_manager/query_state_verifier /
COPY common /common

ENTRYPOINT ["/bin/sh"]
