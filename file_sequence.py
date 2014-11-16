#!/usr/bin/env python
# python 2.6.6

# IMPORTS
import re


# CONSTANTS
WHITE_SPACES = re.compile(r'\s+')
RE_DIGITS = re.compile(r'\d+')
RE_NON_DIGITS = re.compile(r'\D+')
RE_NUM_START = re.compile(r'^\d')
RE_ALPHA_DIGITAL = re.compile(r'(\d+|\D+)')
RE_PATH_SEPARATOR = re.compile(r'(//?|\\\\?)')
RE_EXT = re.compile(r'\.\D+$')
RE_DIRECTORIES = re.compile(r'[\s\S]+?(?://?|\\\\?|$)')# Everything before single and double slashs includingly.


# EXCEPTIONS
class SequenceError(Exception):
	pass
class FileError(Exception):
	pass


# CLASSES
class File(object):
	def __init__(self, path):
		if isinstance(path, File):
			# Data is File, copy attributes
			self.__dict__.update(path.__dict__)
		elif type(path) is str:
			# Data is string, initialise attributes
			self.__path = path
			# Basic attributes based of path
			self.__dir_path = ''
			self.__dir_name = ''
			self.__file_name = ''
			self.__ext = ''
			self.__file_parts = None
			self._set_basic_attr()
			# Sequential attributes, to be assigned later when sequence is found
			self.__head = ''
			self.__number = None
			self.__tail = ''

			self.__padding = None
			self.__number_idx = None
		else:
			# Data is of wrong type, raise exception
			raise TypeError("File argument must be of type str or instance of File class")

	def __repr__(self):
		return "<File: '{0}'>".format(self.__path)


	@property
	def path(self):
		return self.__path
	@property
	def dir_path(self):
		return self.__dir_path
	@property
	def dir_name(self):
		return self.__dir_name
	@property
	def file_name(self):
		return self.__file_name
	@property
	def head(self):
		return self.__head
	@property
	def number(self):
		return self.__number
	@property
	def tail(self):
		return self.__tail
	@property
	def ext(self):
		return self.__ext
	@property
	def padding(self):
		return self.__padding


	def _set_basic_attr(self):
		""" Set basic attributes based on path """
		p = re.findall(RE_DIRECTORIES, self.path)
		self.__dir_path = ''.join(p[:-1])
		self.__dir_name = re.sub(RE_PATH_SEPARATOR, "", p[-2])
		self.__file_name = re.sub(RE_EXT, "",  p[-1])
		self.__ext = re.findall(RE_EXT, p[-1])[0]
		self.__file_parts = re.findall(RE_ALPHA_DIGITAL, self.__file_name)

	def set_number_from_index(self, idx):
		''' Sets number attributes based on index'''
		idx = int(idx)
		num = re.findall(RE_DIGITS, self.file_name)
		try:
			number = int(num[idx])
		except IndexError:
			raise FileError("File number index is out of range")
		pad = len(num[idx])
		alpha = re.findall(RE_NON_DIGITS, self.file_name)
		num_start = re.findall(RE_NUM_START, self.file_name)
		head = tail = ''

		# determine head and tail based on index
		signed_idx = idx if idx < 0 else idx-len(num)
		mod = 1
		if len(num) != abs(signed_idx):
			while len(num) > abs(signed_idx):
				# Head
				if (num_start and mod % 2) or (not num_start and not mod % 2):
					head += num.pop(0)
				else:
					head += alpha.pop(0)
				mod +=1
			else:
				head += alpha.pop(0)
		num.pop(0)
		mod = 0
		while num or alpha:
			# Tail
			if num and mod % 2:
				tail += num.pop(0)
			elif alpha:
				tail += alpha.pop(0)
			mod +=1
		# Assign to self
		self.__number_idx = idx
		self.__number = number
		self.__padding = pad
		self.__head = ''.join(head) if head else ''
		self.__tail = ''.join(tail) if tail else ''

	def get_numerical_differences(self, other):
		""" Returns the index of the numerical differences in a list. The alpha portion of the name must be the same """
		
		pass





class Sequence(object):
	
	def __init__(self, data):
		self.__sequence = data

	def __repr__(self):
		return "<Sequence: '{0}'>".format(sequence_to_compact_string(self.__sequence))

	def __iter__(self):
		return iter(self.__sequence)

	def __getitem__(self, index):
		return self.__sequence[index]

	def __delitem__(self, index):
		self.__sequence.pop(index)

	def __len__(self):
		return len(self.__sequence)
		
	@property
	def sequence(self):
		return self.__sequence

	def __as_list(self):
		return sort(list(set([ i.number for i in self.__sequence ])))
	def match(self, arg):
		pass
	def append(self):
		pass
	def extend(self):
		pass


	



def sequence_to_compact_string(arg = []):
	"""
	Converts a sequence of numbers into a string representation of a compact range
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
	Converts a string representation of a compact range into a sequence of numbers
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
	print(s.sequence)
	m = File("//home//VGMTL//mgaubin//Desktop//Python//file_seq//tests//012_vb_110_v001.0001.png")
	print(m)
	print(m.path)
	mm = File(m)
	print(mm)
	#mm.path = r"\\newpath\newfile.newext"
	print(mm)
	print(m)
	m.set_number_from_index(1)
	d = m.__dict__

	for att in d:
		print(att, d[att])


