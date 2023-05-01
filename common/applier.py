class Applier:
  def __init__(self, operation):
    self.operation = operation

  def apply(self, key, value):
    return self.operation(key, value)

"""
op = lambda k,v: [k, v[0] / v[1]]
mean_applier = Applier(op)
mean_applier.apply('2014-06-12', [378.3, 2])

# ['2014-06-12', 189.15]

op = lambda k,v: [k, v[1] > 2*v[0]]
double_checker = Applier(op)
double_checker.apply("Square St-Louis", [25, 54])

# ["Square St-Louis", True]
"""