class Transformer:
  def __init__(self, columns, conditions):
    keys = columns.split(",")
    new_dict = {}
    for i, key in enumerate(keys):
      if key in conditions:
        new_dict[i] = conditions[key]

    self.conditions = new_dict

  def transform(self, row):
    elems = row.split(',')
    for i, elem in enumerate(elems):
      if i in self.conditions:
        elems[i] = self.conditions[i](elem)

    return elems

class FilterColumns:
	def __init__(self, columns, wanted_columns):
		columns = columns.split(',')
		wanted_columns = wanted_columns.split(',')
		
		self.idxs = [i for i, col in enumerate(columns) if col in wanted_columns]

	def __obtain_idxs(self):
		return [i for i, col in enumerate(self.columns) if col in self.wanted_columns]
	
	def filter(self, columns):
		columns = columns.split(",")
		result = []
	
		for i, col in enumerate(columns):
			if i in self.idxs:
				result.append(col)
				
		return ','.join(result)

class FilterRows:
	def __init__(self, columns, dict_cond):
		keys = columns.split(",")
		new_dict = {}
		for i, key in enumerate(keys):
				if key in dict_cond:
						new_dict[i] = dict_cond[key]

		self.conditions = self.__map_conditions(len(keys), new_dict)

	def __map_conditions(self, max_args, dict_cond):
		conditions = []
		for i in dict_cond:
			conditions = self.__fill_conds(conditions, i)
			conditions.append(dict_cond[i])
		
		return conditions
				
	def __fill_conds(self, conds, next):
		diff_cons = next - len(conds)
		for i in range(len(conds), diff_cons):
			conds.append(True)

		return conds
	
	def filter(self, row):
		elements = row.split(",")
		result = []
		for elem, condition in zip(elements, self.conditions):
			if callable(condition):
				if not condition(elem):
					return None
		return row

"""
columns = 'date,year,code'
dict_cond = {'date': lambda x: x.split(' ')[0]}
f = Transformer(columns, dict_cond)
f.transform('2014-00-00 00:00:00,5454,3')

columns = 'name,year,code'
dict_cond = {'name': lambda x: int(x) != 1, 'year': lambda x: int(x) > 1}
f = FilterRows(columns, dict_cond)
f.filter('1,5454,3')
"""