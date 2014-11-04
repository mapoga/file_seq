
"""
TODO:
	-Clean frame class
	-Being able to create sequence from list of path as well from list of frame object
	-function to output get formatted sequence
	-compress/decompress sequence
	-rename file sequence in directory
	-for images only option

	-Sequences class accepts str, numbers, frame obj as well as list of those instances. Remove create sequences fct. Arg to accept only specific.
	-Verify isinstance inputs before moving on and raise error if wrong instance among the inputs. Stop and return none
	-Frame class should accept str and numbers.
	-Same as format create shorthand to rename
	-Arg to accept format only
	-Rename fct working like formatting. Verify if iy can before doing it.
	-Construct hierarchy from folders in relation to cwd


"""



# ======================================================================
# IMPORTS
# ======================================================================

import os
import re
import pprint
pp = pprint.PrettyPrinter(indent=2)


# ======================================================================
# CONSTANTS
# ======================================================================

reDigits = re.compile(r'\d+')
reNonDigits = re.compile(r'\D+')
reNumStart = re.compile(r'^\d')


# ======================================================================
# EXCEPTIONS
# ======================================================================

class SequenceError(Exception):
	pass

class FrameError(Exception):
	pass


# ======================================================================
# CLASSES
# ======================================================================


class Sequence:
	"""
	Sequence documentation

	"""

	def __init__(self, frames):
		self._dirPath = frames[0].dirPath
		self._dirName = frames[0].dirName
		self._head = frames[0].head
		self._tail = frames[0].tail
		self._padding = frames[0].padding
		self._ext = frames[0].ext
		self._frames = list(set([ f.number for f in frames ]))
		self._frames.sort()
		self._set_first()
		self._set_last()
		self._set_length()
		self._set_missing()
		self._set_range()


	#------ METHODS ----------------------------------------------------

	#---Private getter methods
	def _get_dirPath(self):
		return self._dirPath

	def _get_dirName(self):
		return self._dirName

	def _get_head(self):
		return self._head

	def _get_tail(self):
		return self._tail

	def _get_padding(self):
		return self._padding

	def _get_ext(self):
		return self._ext

	def _get_frames(self):
		return self._frames

	def _get_first(self):
		return self._first

	def _get_last(self):
		return self._last

	def _get_length(self):
		return self._length

	def _get_missing(self):
		return self._missing

	def _get_range(self):
		return self._range


	#---Private setter methods
	def _set_readonly(self, value):
		raise TypeError("Read-only attribute")

	def _set_first(self):
		self._first = self._frames[0]

	def _set_last(self):
		self._last = self._frames[-1]

	def _set_length(self):
		self._length = len(self._frames)

	def _set_missing(self):
		if len(self._frames) > 1 and  self._frames[0]!= None:
			whole = set(range(self._frames[0], self._frames[-1]))
			tmp = list(whole-set(self._frames))
			tmp.sort()
			self._missing = tmp
		else:
			self._missing = []

	def _set_range(self):
		self._range = str( str(self.frames[0]) +'-'+ str(self.frames[-1]) )


	#------ PROPERTIES -------------------------------------------------

	# Read-only immutable public properties
	dirPath = property(_get_dirPath, _set_readonly, doc="Absolute path where the sequence reside")
	dirName = property(_get_dirName, _set_readonly, doc="String of the directory name where the sequence reside")
	head = property(_get_head, _set_readonly, doc="String preceding sequence number")
	tail = property(_get_tail, _set_readonly, doc="String after the sequence number")
	padding = property(_get_padding, _set_readonly, doc="Integer quantity of integers used to describe the sequence number")
	ext = property(_get_ext, _set_readonly, doc="String representing the extension of the file")
	# Read-only mutable public properties
	frames = property(_get_frames, _set_readonly, doc="Integer list of frames in the sequence")
	first = property(_get_first, _set_readonly, doc="Integer number for the first frame of the sequence")
	last = property(_get_last, _set_readonly, doc="Integer number for the last frame of the sequence")
	length = property(_get_length, _set_readonly, doc="Length of the frames list")
	missing = property(_get_missing, _set_readonly, doc="Integer list of frames missing in the sequence")
	range = property(_get_range, _set_readonly, doc="String containning the frame range of the sequence. ex:'1-10' ") 


	#---Public methods
	def match(self, frame):
		# Returns true if both items are of the same sequence
		if self.ext == frame.ext:
			if self.padding == frame.padding:
				if self.head == frame.head:
					if self.tail == frame.tail:
						if self.ext != None:
							if self.padding != None:
								if frame.number:
									return True
		return False

	def contains(self, frame):
		pass

	def append(self, frame):
		if self.match(frame):
			self._frames.append(frame.number)
			self._frames = list(set(self._frames))
			self._frames.sort()
			self._set_first()
			self._set_last()
			self._set_length()
			self._set_missing()
			self._set_range()
		else:
			raise SequenceError('Appending item is not a member of this sequence')

	def formated(self, format):
		pass

	def rename(self, head, padding, tail, ext, offset):
		pass





class Frame:
	"""
	Frame documentation

	"""

	#------ CONSTRUCTOR -------------------------------------------------
	def __init__(self, path):
		# Normalise path
		path = os.path.normcase(path)
		# Assign attributes value 
		self._path = path
		self._dirPath, doc = os.path.split( path )
		self._dirName = os.path.split(self._dirPath)[1]
		self._head = []
		self._tail = []
		self._number = None
		self._padding = None		
		body, self._ext = os.path.splitext(doc)

		self._numStart = True if reNumStart.match( body ) else False
		self._numIndex = None
		self._numSubSet = reDigits.findall( body )
		self._alphaSubSet = reNonDigits.findall( body )
		self._set_subsets()


	#------ METHODS ----------------------------------------------------

	#---Private getter methods
	def _get_path(self):
		return self._path

	def _get_dirPath(self):
		return self._dirPath

	def _get_dirName(self):
		return self._dirName

	def _get_head(self):
		return self._head

	def _get_tail(self):
		return self._tail

	def _get_number(self):
		return self._number

	def _get_padding(self):
		return self._padding

	def _get_ext(self):
		return self._ext


	#---Private setter methods
	def _set_readonly(self, value):
		raise TypeError("Read-only attribute")

	def _set_subsets(self):
		tmpNum = list(self._numSubSet)
		tmpAlpha = list(self._alphaSubSet)
		subsets = []
		i = 1
		while tmpNum or tmpAlpha:
			if (self._numStart and i%2) or (not self._numStart and not i%2):
				subsets.append(tmpNum.pop(0))
			else:
				subsets.append(tmpAlpha.pop(0))
			i+=1
		self._subsets = list(subsets)


	#------ PROPERTIES -------------------------------------------------

	# Read-only immutable public properties
	path = property(_get_path, _set_readonly, doc="Absolute path of the file")
	dirPath = property(_get_dirPath, _set_readonly, doc="Absolute path where the sequence reside")
	dirName = property(_get_dirName, _set_readonly, doc="String of the directory name where the sequence reside")
	head = property(_get_head, _set_readonly, doc="String preceding sequence number")
	tail = property(_get_tail, _set_readonly, doc="String after the sequence number")
	number = property(_get_number, _set_readonly, doc="Integer number of the file within a sequence")
	padding = property(_get_padding, _set_readonly, doc="Integer quantity of integers used to describe the sequence number")
	ext = property(_get_ext, _set_readonly, doc="String representing the extension of the file")
	

	#---Public methods
	def set_num_index(self, ind):
		"""
		Sets the index deciding which numerical part of the name string will be chosen for the numerotation.
		ex:  "shot50_beauty_v001.0034.png"
		An index of 1 would refer to '50' and an index of -1 would refer to '0034'.
		Automatically assign the corresponding head, number, padding and tail properties
		An index with value None will have all in the head and no tail. number will be None and padding will be None.
		"""
		if self._numSubSet:
			if abs(ind) <= len(self._numSubSet):
				#map index
				if ind > 0:
					ind -= 1
					unsignedInd = ind
				else:
					unsignedInd = len(self._numSubSet)+ind
				#assign attributes
				self._numIndex = ind
				self._number = int(self._numSubSet[self._numIndex])
				self._padding = len(self._numSubSet[self._numIndex])
				tmpNum = list(self._numSubSet)
				tmpAlpha = list(self._alphaSubSet)
				#Loop through digital and nonDigital parts to create head and tail
				#head
				d = 0
				while unsignedInd >= len(self._numSubSet)-len(tmpNum) and (tmpAlpha or tmpNum):
					if (self._numStart and not d%2) or (not self._numStart and d%2):
						if unsignedInd == len(self._numSubSet)-len(tmpNum):
							del tmpNum[0]
						else:				
							self._head.append(tmpNum.pop(0))
					else:
						self._head.append(tmpAlpha.pop(0))
					d += 1
				#tail
				d = 0
				while tmpAlpha or tmpNum:
					if not d%2:
						self._tail.append(tmpAlpha.pop(0))
					else:
						self._tail.append(tmpNum.pop(0))
					d += 1
				return
		# If index out of range
		# If no numerical value
		# If ind is None ( alone without sequence )
		# put everyting in head
		tmpNum = list(self._numSubSet)
		tmpAlpha = list(self._alphaSubSet)
		d = 1
		while tmpAlpha or tmpNum:
			if (self._numStart and d%2) or (not self._numStart and not d%2):
				if tmpNum:
					self._head.append(tmpNum.pop(0))
				else:
					self._head.append(tmpAlpha.pop(0))
			else:
				if tmpAlpha:
					self._head.append(tmpAlpha.pop(0))
				else:
					self._head.append(tmpNum.pop(0))


	def differences(self, fr):
		"""
		Returns the index of the numSubset where there is only one numerical difference
		If alphaSubset is the same and single difference in numSubset
		If more than one difference, returns None
		"""

		if len(self._subsets) == len(fr._subsets):
			if self._alphaSubSet == fr._alphaSubSet:
				if len(self._numSubSet) == len(self._numSubSet):
					i = 0
					diff = []
					while i < len(self._numSubSet):
						if self._numSubSet[i] != fr._numSubSet[i]:
							diff.append( i+1 )
						i+=1

					if len(diff) > 1 or len(diff) < 1:
						return None
					else:
						return diff[0]
		return None


	def match(self, sequence):
		if self.ext == sequence.ext:
			if self.padding == sequence.padding:
				if self.head == sequence.head:
					if self.tail == sequence.tail:
						if self.ext != None:
							if self.padding != None:
								return True
		return False



# Module functions

def get_frames_from_directory(dir):
	# returns a list of frame objects
	dir = os.path.normcase( dir )
	files = os.listdir(dir)
	files.sort()
	seq =[]
	if files:
		for f in files:
			p = os.path.join(dir, f)
			if os.path.isfile(p):
				try:
					seq.append( Frame( p ) )
				except FrameError:
					pass
		return seq
	else:
		return []


def sequences_from_files( frames, strict_ind = False, ind = -1 ):
	"""
	Returns a list of sequences
	Takes str and Frame types or list of any of the two. Can be mixed.

	"""

	if not isinstance(frames, list):
		frames = [frames]
	else:
		for i in frames:
			if not (isinstance(i, str) or isinstance(i, Frame) ):
				print(isinstance(i, Frame), i, i.path, type(i))
				raise TypeError("Wrong type: Should be str, Frame or list of any of the two!")
				return		

	if frames:
		sequences = []

		# for each frame find the biggest trend and create a sequence from it or append to it
		f = 0
		trends = [] 
		# each frame loop
		while f < len(frames):
			if not strict_ind:	
				ff = 0
				trends = []
				while ff < len(frames):
					#comparison
					if ff != f:
						t = frames[f].differences(frames[ff])
						if t != None:
							trends.append( t )
					ff+=1
				# Find the trend
				if trends:
					trend = max(set(trends), key=trends.count)
					# Set the frame to that trend
					frames[f].set_num_index(trend)
				else:
					# no trend, take default index
					frames[f].set_num_index(ind)
			else:
				# index from strict
				frames[f].set_num_index(ind)

			# Add to a sequence or create one
			match = False
			if sequences:
				for s in sequences:
					if s.match(frames[f]):
						s.append(frames[f])
						match = True

			if not sequences or not match:
				seq = Sequence([ frames[f] ])
				sequences.append(seq)

			f+=1
		return sequences
	return []



def compress(): # from [1,2,3,4,6,8,18,19,20,22] to '1-3,4-8x2,18-20,22'
	pass

def decompress(): # from '1-3,4-8x2,18-20,22' to [1,2,3,4,6,8,18,19,20,22]
	pass


if __name__ ==  "__main__":



	p = os.path.normcase("P:/Programming/Python/seq/tests")
	#p = os.path.normcase("P:/Programming/Python/seq/tests/small")
	f = get_frames_from_directory(p)

	#print(s[0]._dict_)
	#pp.pprint(s[0]._dict_)
	
	s = sequences_from_files(f)
	print('LEN: ', len(s) )

	for item in s:
		pp.pprint(item.__dict__)
		#print(item.padded_path(), len(item.frames))
		print(" ")

	"""
	print(s[9])
	pp.pprint(s[1]._dict_)
	print(s[1].range)
	"""