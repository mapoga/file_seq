#!/usr/bin/env python
# python 2.6.6

import re

WHITE_SPACES = re.compile(r'\s+')

class Sequence:

	def __init__(self, data):
		self.sequence = data

	def __repr__(self):
		return "<Sequence: '{0}'>".format(sequence_to_compact_string(self.sequence))

	def __iter__(self):
		return iter(self.sequence)

	def __getitem__(self, index):
		return self.sequence[index]

	def __delitem__(self, index):
		self.sequence.pop(index)

	def __len__(self):
		return len(self.sequence)

	def __as_list(self):
		return sort(list(set([ i.number for i in self.sequence ])))


	def append(self):
		pass
	def extend(self):
		pass


	
	
def sequence_to_compact_string(arg = []):
	"""
	Converts a sequence of numbers into a range string representation
	sequence_to_compact_string([1,2,3,11,12,20,22,24,25]) >>> "1-3,11,12,20-24x2,25"
	"""
	# Verify arg type, remove duplicates & sort
	try:
		numbers = sorted(list(set([int(n) for n in arg])))
	except ValueError:
		raise ValueError("Sequence must contain only numbers")
	except TypeError:
		raise TypeError("Sequence must be an iterable")
	
	def format_rule(start, end, step):
		"""  format rule as 'N', N-N or N-NxN  """
		if  end-start == 0:
			return "{0}".format(start)
		elif step == 1:
			return "{0}-{1}".format(start, end)
		else:
			return "{0}-{1}x{2}".format(start, end, step)
			
	def sub_rule(numbers = []):
		"""  returns list of sub sequence defined by a rule   """
		start = end = numbers[0]
		step = None
		for i, n in enumerate(numbers[1:]):
			if step == None or n-end == step:
				# continue the loop until step is different
				step = n-end
				end = n
			else:
				if step == end-start:
					# sub_rule is only two numbers long,
					# yield and start from current
					yield start, start, step
					start = end
					end = n
					step = end-start				
				else:
					# yield sequence
					yield start, end, step
					start = end = n
					step = None
		else:
			# last iteration
			if step == end-start:
				# sub_rule is only two numbers long,
				# yield separate
				yield start, start, step
				yield end, end, step
			else:
				# yield single or sequence
				yield start, end, step
	return ','.join([format_rule(*i) for i in sub_rule(arg)])
	
def compact_string_to_sequence(string=""):
	"""
	Converts a range string representation into a sequence of numbers
	compact_string_to_sequence("1-3,11,12,20-24x2,25") >>> [1,2,3,11,12,20,22,24,25]
	"""
	# verify arg type is string
	if string is isinstance(string, basestring):
		raise TypeError("Argument must be string")
		
	def string_rule_to_sequence(rule = ''):
		"""  Convert a compact string sequence rule into a list  """
		if 'x' in rule:
			# Apply rule to range
			rule = re.split(r"[x,X]", rule)
			start, end = re.split(r"\-", rule[0])
			return [s for s in range(int(start),int(end)+1) if (s-int(start)) % int(rule[-1]) == 0]
		elif '-' in rule:
			# get range
			start, end = re.split(r"\-", rule)
			return range(int(start),int(end)+1)
		else:
			# single value
			return [int(rule)]
	# Remove whitespaces and return a list of int from unpacked sub ranges
	return [i for sub_i in [string_rule_to_sequence(e) for e in re.split(r'\,',re.sub(WHITE_SPACES, "", string))] for i in sub_i ]








if __name__ == "__main__":
	s = Sequence([1,2,3,4,5,6,7,8,9,10])
	print(s)
	for i in s:
		pass
		#print(i)
	print(s[5])
	del s[5]
	print(s)
	print(len(s))
