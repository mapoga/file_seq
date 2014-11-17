#!/usr/bin/env python
# python 2.6.6

'''
TODO:
	# filter by index using builtin filter
	# Sequence init more friendly
	# ie accepts single and iterable (str, Numbered_file)
	# verify NumberedFile init
	# Implement Sequence.pop() 
'''



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

FORMAT_NUMBERED_FILE = "{DIRp}{HEAD}{NUMp}{TAIL}{EXT}"
FORMAT_SEQUENCE_COMPACT = "{DIRp}{HEAD}{PAD#}{TAIL}{EXT} {NUMc}"
FORMAT_SEQUENCE_RANGE = "{DIRp}{HEAD}{PAD#}{TAIL}{EXT} {NUMr}"
FORMAT_SEQUENCE_REPR = "..{SEP}{DIRn}{SEP}{HEAD}{PAD#}{TAIL}{EXT} {NUMc}"

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
		return "<NumberedFile: {0}>".format(self.path)

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
	@property
	def number_index(self):
		return self._number_idx

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
		''' Sets number attributes based on index
		If index is out of range, an error will be raised
		'''
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
		if len(num) != abs(signed_idx) or len(num) == 1:
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
		if len(self._file_parts) == len(other._file_parts):
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
		""" Accepts Sequence or NumberedFile
		Return true is both are ready to be part of the same sequence """
		if self.padding and other.padding:
			if self.dir_path == other.dir_path:
				if self.head == other.head:
					if self.padding == other.padding:
						if self.tail == other.tail:
							if self.ext == other.ext:
								if self._number_idx == other._number_idx:
									return True
		return False

	def _FORMATING(self):
		return {
			"SEP": str(re.findall(RE_PATH_SEPARATOR, self.path)[-1]) if re.findall(RE_PATH_SEPARATOR, self.path) else str(os.sep),
			"PATH": self.path,
			"DIRp": self.dir_path,
			"DIRn": self.dir_name,
			"HEAD": self.head,
			"PAD": str(self.padding),
			"PAD#": ''.join(["#" for i in range(self.padding)]),
			"PAD%": '%{0:0=2d}d'.format(self.padding),
			"TAIL": self.tail,
			"EXT": self.ext,
			"NUM": str(self.number),
			"NUMp": '{0:0=-{1}d}'.format(self.number, self.padding)
			}

	def formatted(self, format_str=FORMAT_NUMBERED_FILE):
		"""
		{SEP} = Paths separator >>>"/"
		{PATH} = Full original path
		{DIRp} = Directory path
		{DIRn} = Directory name
		{HEAD} = String preceding sequence number
		{TAIL} = String succeding sequence number
		{EXT} = Extension >>> ".png"
		{PAD} = Padding quantity >>> 4
		{PAD#} = Padding representation >>> '####'
		{PAD%} = Padding representation >>> '%04d'
		{NUM} = Number  >>> '1'
		{NUMp} = Number padded >>> '0001'

		Default formatting:
		>>>  "{DIRp}{HEAD}{NUMp}{TAIL}{EXT}"
		"""
		return format_str.format(**self._FORMATING())




class Sequence(object):
	'''
		Accepts an iterable containing a single sequence of NumberedFiles
		Converts strings into NumberedFiles.
		If there is no numerical components, an NumberedFileError will be raised
		If sequence members dont match a SequenceError will be raised

		Returns a 
	'''
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
	
	def __init__(self, data, idx=-1):
		try:
			s = [ NumberedFile(i) for i in data ]
			self.__sequence = s
			self.__sort_sequence()
			self._number_idx = data[0]._number_idx
		except IndexError:
			raise SequenceError("Sequence() argument must be an iterable containing NumberedFiles or string")

	def __repr__(self):
		return "<Sequence: {0}>".format( self.formatted(FORMAT_SEQUENCE_REPR) )

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
	def len(self):
		return len(self.sequence)
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
	@property
	def number_index(self):
		return self.sequence[0].number_index
	@property
	def numbers(self):
		return [ i.number for i in self.sequence ]
	@property
	def numbers_missing(self):
		return sorted(list(set(range(self.sequence[0].number, self.sequence[-1].number+1))-set(self.numbers)))
	@property
	def missing(self):
		return [ NumberedFile( self.formatted("{DIRp}{HEAD}")+"{0:0=-{1}d}".format(i, self.padding)+self.formatted("{TAIL}{EXT}")) for i in self.numbers_missing] if self.numbers_missing else []

	def is_match(self, other):
		""" Accepts Sequence or NumberedFile
		Return true is both are ready to be part of the same sequence """
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
		''' Appends a NumberedFile to the sequence if its a match
		Otherwise a SequenceError is raised '''
		if self.is_match(other):
			self.__sequence.append(other)
			self.__sort_sequence()
		else:
			raise SequenceError("Argument does not match sequence")

	def extend(self, other):
		''' Extend a Sequence to the sequence if its a match
		Otherwise a SequenceError is raised '''
		if self.is_match(other):
			self.__sequence.extend(other)
			self.__sort_sequence()
		else:
			raise SequenceError("Argument does not match sequence")

	def pop():
		NotImplemented
		pass

	def formatted(self, format_str=FORMAT_SEQUENCE_RANGE):
		"""
		{SEP} = Paths separator >>>"/"
		{DIRp} = Directory path
		{DIRn} = Directory name
		{HEAD} = String preceding sequence number
		{TAIL} = String succeding sequence number
		{EXT} = Extension >>> ".png"
		{PAD} = Padding quantity >>> 4
		{PAD#} = Padding representation >>> '####'
		{PAD%} = Padding representation >>> '%04d'
		{NUM} = Sequence numbers joined by ','. >>> '1,2,3,4'
		{NUMc} = Sequence numbers in compact form >> '1-3,11,20-24x2'
		{NUMr} = Sequence numbers range >> '1-24'
		{LEN} = Quantiy of items in sequence
		{FIRST} = First number of the sequence >>> '1'
		{LAST} = Last number of the sequence >>> '24'
		{MISS} = Missing sequence numbers >>> '3,4,5,7'
		{MISSc} = Missing sequence numbers in compact form >>> '3-5,7'
		{MISSr} = Missing sequence numbers range >>> '3-7'

		Default formatting:
		>>>  "{DIRp}{HEAD}{PAD#}{TAIL}{EXT} {NUMr}"
		"""
		return format_str.format(**self._FORMATING())

	def _FORMATING(self):
		return {
			"SEP": str(re.findall(RE_PATH_SEPARATOR, self.path)[-1]) if re.findall(RE_PATH_SEPARATOR, self.path) else str(os.sep),
			"DIRp": self.dir_path,
			"DIRn": self.dir_name,
			"HEAD": self.head,
			"PAD": str(self.padding),
			"PAD#": ''.join(["#" for i in range(self.padding)]),
			"PAD%": '%{0:0=2d}d'.format(self.padding),
			"TAIL": self.tail,
			"EXT": self.ext,
			"FIRST": str(self.sequence[0].number),
			"LAST": str(self.sequence[-1].number),
			"NUM": ','.join([ str(i) for i in self.numbers]),
			"NUMc": sequence_to_compact_string(self.numbers),
			"NUMr": "{0}-{1}".format(self.sequence[0].number, self.sequence[-1].number+1),
			"LEN": str(self.len),
			"MISS": ','.join([ str(i) for i in self.numbers_missing]) if self.numbers_missing else '',
			"MISSc": sequence_to_compact_string(self.numbers_missing) if self.numbers_missing else '',
			"MISSr": "{0}-{1}".format(self.numbers_missing[0], self.numbers_missing[-1]+1) if self.numbers_missing else '',
			}		

	def __sort_sequence(self):
		self.__sequence = sorted(list(set(self.sequence)), key=lambda item: item.number )




def sequence_to_compact_string(arg = [], steps=True):
	"""
	Converts a sequence of numbers into a string representation in a compact range
	sequence_to_compact_string([1,2,3,11,12,20,22,24,25]) >>> "1-3,11,12,20-24x2,25"
	If steps is True, sequence with a step higher than 1 will be recognised. [20,22,24] >>> 20-24x2
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
			if step == None or (n-end == step and (steps or step == 1)):
				# continue the loop until step is different or steps is False
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
	return sorted(files)

def sequences_from_files (paths, idx=-1 ):
	"""
	Takes a collection of paths or NumberedFiles and converts it in a list of sequence(s)
	Retains only files that are numbered.
	When no sequence is found, idx determines the number among the nummerical parts of the filename.
	'Layer_01_Beauty_02_v003.tiff' >>> nummerical parts=['01', '02', '003'] >>> idx -1 >>> number will be 3.
	"""
	paths = sorted(list(set([NumberedFile(str(p)) for p in paths if re.findall(RE_DIGITS, str(p))])), key=lambda item: item.path  )
	sequences = []
	for index, path in enumerate(paths):
		# list numerical index for possible matchs
		matchs = [ p.get_numerical_parts_differences(path)[0] for p in paths if( (p.path != path.path) and (len(path.get_parts_differences(p)) == 1) and (not path.get_alpha_parts_differences(p)) )]

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
	m1 = NumberedFile("//home//VGMTL//mgaubin//Desktop//Python//file_seq//tests//012_vb_110_v001_01.0001.png")
	m2 = NumberedFile("//home//VGMTL//mgaubin//Desktop//Python//file_seq//tests//012_vb_110_v001_01.0002.png")
	m3 = NumberedFile("//home//VGMTL//mgaubin//Desktop//Python//file_seq//tests//012_vb_110_v001_01.0003.png")
	m1.set_number_from_index()
	m2.set_number_from_index()
	m3.set_number_from_index()
	files = files_from_directory(r"P:\Programming\Python\seq\scripts\file_seq\tests\all_cripled")
	"""
	blop = NumberedFile( files[0] )
	blob = NumberedFile( files[1] )
	blop.set_number_from_index()
	blob.set_number_from_index()
	print(blop)
	print(blob)
	s = Sequence([blop])
	"""
	#print(files)
	seq = sequences_from_files(files)
	print('')

	for i in seq:
		print(i.number_index, i)
	
