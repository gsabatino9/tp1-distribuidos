class Groupby:
  def __init__(self, operation, base_data=0):
    self.grouped_data = {}
    self.operation = operation
    self.base_data = base_data

  def add_data(self, group_key, group_value):
    if not group_key in self.grouped_data:
      self.grouped_data[group_key] = self.base_data

    self.grouped_data[group_key] = self.operation(self.grouped_data[group_key], group_value)

"""
group_key = "2014-06-12"
group_value = 165.3
operation = lambda old, new: [old[0]+new, old[1]+1]
base_data = [0,0]

g = Groupby(operation, base_data)
g.add_data(group_key, group_value)

group_key, group_value = "2014-06-12", 213
g.add_data(group_key, group_value)

g.grouped_data
"""