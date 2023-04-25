class FilterColumns:
	def __init__(self, columns):
		self.columns = columns.split(',')

	def __obtain_idxs(self, filtered_columns):
		filtered_columns = filtered_columns.split(',')
		return [i for i, col in enumerate(self.columns) if col in filtered_columns]
	
	def filter(self, filtered_columns, columns):
		columns = columns.decode('utf-8').split(",")
		idxs = self.__obtain_idxs(filtered_columns)
		result = []
	
		for i, col in enumerate(columns):
			if i in idxs:
				result.append(col)
				
		return bytes(','.join(result), 'utf-8')

class FilterRows:
	def __init__(self, max_args, dict_cond):
		self.conditions = self.__map_conditions(max_args, dict_cond)

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
		elements = row.decode('utf-8').split(",")
		result = []
		for elem, condition in zip(elements, self.conditions):
			if callable(condition):
				if not condition(elem):
					return True
		return False