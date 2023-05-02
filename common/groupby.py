from common.connection import Connection
from common.eof_manager import EOF_MSG, WORKER_DONE_MSG
from common.utils import *

class Groupby:
  def __init__(self, operation, base_data=0):
    self.grouped_data = {}
    self.operation = operation
    self.base_data = base_data

  def add_data(self, group_key, group_value):
    if not group_key in self.grouped_data:
      self.grouped_data[group_key] = self.base_data

    self.grouped_data[group_key] = self.operation(self.grouped_data[group_key], group_value)

class GroupbyController:
  def __init__(self, recv_queue, send_queue, em_queue, operation, base_data, gen_key_value):
    self.groupby = Groupby(operation, base_data)
    self.gen_key_value = gen_key_value

    self.__connect(recv_queue, send_queue, em_queue)
    self.recv_queue.receive(self.agroup_data, auto_ack=False)
    self.connection.start_receiving()

  def __connect(self, recv_queue, send_queue, em_queue):
    self.connection = Connection()
    self.recv_queue = self.connection.basic_queue(recv_queue)
    self.em_queue = self.connection.pubsub_queue(em_queue)
    self.em_queue.send(recv_queue)

    self.send_queue = self.connection.basic_queue(send_queue)

  def agroup_data(self, ch, method, properties, body):
    msg = decode(body)

    if msg == EOF_MSG:
      self.__eof_arrived(ch, method.delivery_tag)
    else:
      self.__data_arrived(msg, ch, method.delivery_tag)

  def __eof_arrived(self, ch, delivery_tag):
    print('EOF arrived')
    for data in self.groupby.grouped_data:
      value = self.groupby.grouped_data[data]
      msg = data + ',' + str(value[0]) + ',' + str(value[1])
      self.send_queue.send(msg)

    self.connection.stop_receiving()
    ch.basic_ack(delivery_tag = delivery_tag)
    self.em_queue.send(WORKER_DONE_MSG)

  def __data_arrived(self, msg, ch, delivery_tag):
    key, value = self.gen_key_value(msg)

    self.groupby.add_data(key, value)
    ch.basic_ack(delivery_tag = delivery_tag)
