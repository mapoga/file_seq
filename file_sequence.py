#!/usr/bin/env python
# python 2.6.6

# IMPORTS
import re
import os


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
class NumberedFileError(Exception):
	pass


# CLASSES
class NumberedFile(object):

	def __new__(cls,arg):
		if isinstance(arg, cls):
			return arg
		elif type(arg) is str:
			return object.__new__(cls)
		else:
			raise TypeError("Argument must be String")

	def __init__(self, path):
		if not isinstance(path, NumberedFile):
			self.__path = path
			# Basic attributes based of path
			self.__dir_path = ''
			self.__dir_name = ''
			self.__file_name = ''
			self.__ext = ''
			self._file_parts = None
			self._num_parts = None
			self._non_num_parts = None
			self._set_basic_attr()
			# Sequential attributes, to be assigned later when sequence is found
			self.__head = ''
			self.__number = None
			self.__tail = ''

			self.__padding = None
			self._number_idx = None

	def __repr__(self):
		return "<NumberedFile: '{0}'>".format(self.__path)

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
		self._file_parts = re.findall(RE_ALPHA_DIGITAL, self.__file_name)
		self._num_parts = re.findall(RE_DIGITS, self.__file_name)
		self._non_num_parts = re.findall(RE_NON_DIGITS, self.__file_name)
		if not self._num_parts:
			raise NumberedFileError("Path should have a numerical component to be considered a NumberedFile ")

	def set_number_from_index(self, idx = -1):
		''' Sets number attributes based on index'''
		idx = int(idx)
		num = re.findall(RE_DIGITS, self.file_name)
		try:
			number = int(num[idx])
		except IndexError:
			raise NumberedFileError("NumberedFile number index is out of range")
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
		self._number_idx = idx
		self.__number = number
		self.__padding = pad
		self.__head = ''.join(head) if head else ''
		self.__tail = ''.join(tail) if tail else ''
  
	def get_parts_differences(self, other):
		""" Returns the index of the differences in a list."""
		if len(p) == len(other._file_parts):
			return [ i for i,e in enumerate(self._file_parts) if e != other._file_parts[i] ]
		else:
			return self._file_parts[:]

	def get_numerical_parts_differences(self, other):
		""" Returns the index of the numerical parts differences in a list."""
		if len(self._num_parts) == len(other._num_parts):
			return [ i for i,e in enumerate(self._num_parts) if e != other._num_parts[i] ]
		else:
			return self._num_parts[:]

	def get_alpha_parts_differences(self, other):
		""" Returns the index of the non-numerical parts differences in a list."""
		if len(self._non_num_parts) == len(other._non_num_parts ):
			return [i for i,e in enumerate(self._non_num_parts) if e != other._non_num_parts [i] ]
		else:
			return self._non_num_parts[:]

	def is_match(self, other):
		if self.padding and other.padding:
			if self.dir_path == other.dir_path:
				if self.head == other.head:
					if self.padding == other.padding:
						if self.tail == other.tail:
							if self.ext == other.ext:
								if self._number_idx == other._number_idx:
									return True
		return False




class Sequence(object):

	def __new__(cls, data):
		try:
			is_iter = iter(data)
		except TypeError:
			is_iter = False
		if isinstance(data, cls):
			return data
		elif is_iter:
			return object.__new__(cls)
		elif isinstance(data, NumberedFile):
			return object.__new__(cls)
		elif type(data) is str:
			return NumberedFile.__new__(cls)
		else:
			raise TypeError("Argument must be iterable")
	
	def __init__(self, data):
		self.__sequence = [ NumberedFile(i) for i in data ]
		self.__sort_sequence()
		self._number_idx = data[0]._number_idx

	def __repr__(self):
		return "<Sequence: '{0}'>".format( sequence_to_compact_string(self.__as_list() ) )

	def __iter__(self):
		return iter(self.__sequence)

	def __getitem__(self, index):
		return self.__sequence[index]

	def __delitem__(self, index):
		self.__sequence.pop(index)

	def __len__(self):
		return len(self.sequence)
		
	@property
	def sequence(self):
		return self.__sequence[:]

	@property
	def path(self):
		return self.sequence[0].path
	@property
	def dir_path(self):
		return self.sequence[0].dir_path
	@property
	def dir_name(self):
		return self.sequence[0].dir_name
	@property
	def head(self):
		return self.sequence[0].head
	@property
	def tail(self):
		return self.sequence[0].tail
	@property
	def ext(self):
		return self.sequence[0].ext
	@property
	def padding(self):
		return self.sequence[0].padding


	def __as_list(self):
		return [ i.number for i in self.__sequence ]

	def __sort_sequence(self):
		self.__sequence = sorted(list(set(self.sequence)), key=lambda item: item.number )

	def is_match(self, other):
		if self.padding and other.padding:
			if self.dir_path == other.dir_path:
				if self.head == other.head:
					if self.padding == other.padding:
						if self.tail == other.tail:
							if self.ext == other.ext:
								if self._number_idx == other._number_idx:
									return True
		return False

	def append(self, other):
		if self.is_match(other):
			self.__sequence.append(other)
			self.__sort_sequence()
		else:
			raise SequenceError("Argument does not match sequence")

	def extend(self, other):
		if self.is_match(other):
			self.__sequence.extend(other)
			self.__sort_sequence()
		else:
			raise SequenceError("Argument does not match sequence")


	



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
	return ','.join([format_rule(*i) for i in sub_rule(numbers)])
	
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

def files_from_directory(path):
	files = []
	for root, dirs, filesList in os.walk(path):
		if filesList:
			for f in filesList:
				files.append(os.path.join(root, f))
	return files

def sequences_from_files (paths, idx=-1 ):
	"""
	Takes a collection of paths and converts it in a list of sequence(s)
	Retains only files that are numbered.
	"""
	paths = sorted(list(set([NumberedFile(str(p)) for p in paths if re.findall(RE_DIGITS, str(p))])))
	sequences = []
	for index, path in enumerate(paths):
		# list numerical index for possible matchs
		matchs = [ p.get_numerical_parts_differences(path)[0] for p in paths if path.is_match(p) and p != path and path.get_parts_differences(p) == 1 and (not path.get_alpha_parts_differences(p)) ]
		# find the most common
		if matchs:
			trend = max(set(matchs), key=matchs.count)
		else:
			trend = idx
		# set number index
		path.set_number_from_index(trend)

		# Append to matching sequence or create new
		if sequences:
			is_match = False
			for seq in sequences:
				if path.is_match(seq):
					# Macth found, append to it
					seq.append(path)
					is_match = True
			if not is_match:
				# Match not found, creat new sequence
				sequences.append(Sequence([path]))
		else:
			# No sequence yet, create new one
			sequences.append(Sequence([path]))
	return sequences







if __name__ == "__main__":
	m = NumberedFile("//home//VGMTL//mgaubin//Desktop//Python//file_seq//tests//012_vb_110_v001.0001.png")
	print(m)
	mm = NumberedFile(m)

	print(m.path)
	mm = NumberedFile(m)
	m1 = NumberedFile("//home//VGMTL//mgaubin//Desktop//Python//file_seq//tests//012_vb_110_v001_01.0001.png")
	m2 = NumberedFile("//home//VGMTL//mgaubin//Desktop//Python//file_seq//tests//012_vb_110_v001_01.0002.png")
	m3 = NumberedFile("//home//VGMTL//mgaubin//Desktop//Python//file_seq//tests//012_vb_110_v001_01.0003.png")
	m1.set_number_from_index()
	m2.set_number_from_index()
	m3.set_number_from_index()
	"""
	d = m2.__dict__
	for att in d:
		print(att, d[att])
	"""
	files = files_from_directory(r"P:\Programming\Python\seq\scripts\file_seq\tests\small")
	print(files)
	seq = sequences_from_files(files)
	print('')
	print(seq)
