from common.connection import Connection
from common.eof_manager import EOF_MSG, WORKER_DONE_MSG
from common.utils import *

class Applier:
  def __init__(self, operation):
    self.operation = operation

  def apply(self, key, value):
    return self.operation(key, value)

class ApplierController:
  def __init__(self, recv_queue, em_queue, send_queue, operation, gen_result_msg, id_query):
    self.id_query = id_query
    self.gen_result_msg = gen_result_msg
    self.applier = Applier(operation)
    self.__connect(recv_queue, em_queue, send_queue)
    self.recv_queue.receive(self.recv_data_to_apply, auto_ack=False)
    self.conn.start_receiving()

  def __connect(self, recv_queue, em_queue, send_queue):
    self.conn = Connection()
    self.recv_queue = self.conn.basic_queue(recv_queue)
    self.send_queue = self.conn.routing_queue(send_queue)

    self.em_queue = self.conn.pubsub_queue(em_queue)
    self.em_queue.send(recv_queue)

  def recv_data_to_apply(self, ch, method, properties, body):
    msg = decode(body)
    if msg == EOF_MSG:
      self.__eof_arrived(ch, method.delivery_tag)
    else:
      self.__apply(msg, ch, method.delivery_tag)

  def __eof_arrived(self, ch, delivery_tag):
    self.em_queue.send(WORKER_DONE_MSG)
    self.conn.stop_receiving()
    ch.basic_ack(delivery_tag = delivery_tag)
    
  def __apply(self, msg, ch, delivery_tag):
    result, msg_to_send = self.gen_result_msg(msg, self.applier)
    if result:
      self.send_queue.send(msg_to_send, routing_key=self.id_query)

    ch.basic_ack(delivery_tag = delivery_tag)