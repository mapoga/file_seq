import os
import re
import pprint
pp = pprint.PrettyPrinter(indent=2)



"""
TODO:
	-Clean frame class
	-Being able to create sequence from list of path as well from list of frame object
	-function to output get formatted sequence
	-compress/decompress sequence
	-rename file sequence in directory
	-for images only option
"""

# regex
reDigits = re.compile(r'\d+')
reNonDigits = re.compile(r'\D+')
reNumStart = re.compile(r'^\d')

# Exceptions
class SequenceError(Exception):
	pass

class Sequence:
	'Sequence class doc'

	def __init__(self, frames):

		self.__dirPath = frames[0].dirPath
		self.__dirName = frames[0].dirName
		self.__head = frames[0].head
		self.__tail = frames[0].tail
		self.__padding = frames[0].padding
		self.__ext = frames[0].ext
		self.__frames = list(set([ f.number for f in frames ]))
		self.__frames.sort()
		self.__update_first()
		self.__update_last()
		self.__update_length()
		self.__update_missing()
		self.__update_range()


	# Private methods
	def _get_dirPath(self):
		return self.__dirPath

	def _get_dirName(self):
		return self.__dirName

	def _get_head(self):
		return self.__head

	def _get_tail(self):
		return self.__tail

	def _get_padding(self):
		return self.__padding

	def _get_ext(self):
		return self.__ext

	def _get_frames(self):
		return self.__frames

	def _get_first(self):
		return self.__first

	def _get_last(self):
		return self.__last

	def _get_length(self):
		return self.__length

	def _get_missing(self):
		return self.__missing

	def _get_range(self):
		return self.__range

	def _set_readonly(self, value):
		raise TypeError("Read-only attribute")

	# Read-only immutable public attributes
	dirPath = property(_get_dirPath, _set_readonly, doc="Absolute path where the sequence reside")
	dirName = property(_get_dirName, _set_readonly, doc="String of the directory name where the sequence reside")
	head = property(_get_head, _set_readonly, doc="String preceding sequence number")
	tail = property(_get_tail, _set_readonly, doc="String after the sequence number")
	padding = property(_get_padding, _set_readonly, doc="Integer quantity of integers used to describe the sequence number")
	ext = property(_get_ext, _set_readonly, doc="String representing the extension of the file")
	# Read-only mutable public attributes
	frames = property(_get_frames, _set_readonly, doc="Integer list of frames in the sequence")
	first = property(_get_first, _set_readonly, doc="Integer number for the first frame of the sequence")
	last = property(_get_last, _set_readonly, doc="Integer number for the last frame of the sequence")
	length = property(_get_length, _set_readonly, doc="Length of the frames list")
	missing = property(_get_missing, _set_readonly, doc="Integer list of frames missing in the sequence")
	range = property(_get_range, _set_readonly, doc="String containning the frame range of the sequence. ex:'1-10' ") 

	def __update_first(self):
		self.__first = self.__frames[0]

	def __update_last(self):
		self.__last = self.__frames[-1]

	def __update_length(self):
		self.__length = len(self.__frames)

	def __update_missing(self):
		if len(self.__frames) != 1 and  self.__frames[0]!= None:
			whole = set(range(self.__frames[0], self.__frames[-1]))
			tmp = list(whole-set(self.__frames))
			tmp.sort()
			self.__missing = tmp
		else:
			self.__missing = []

	def __update_range(self):
		self.__range = str( str(self.frames[0]) +'-'+ str(self.frames[-1]) )



	# Public methods
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
			self.__frames.append(frame.number)
			self.__frames = list(set(self.__frames))
			self.__frames.sort()
			self.__update_first()
			self.__update_last()
			self.__update_length()
			self.__update_missing()
			self.__update_range()
		else:
			raise SequenceError('Item is not a member of this sequence')

	def formated(self, format):
		pass

	def rename(self, head, padding, tail, ext, offset):
		pass





class Frame:
	'Frame class doc'

	#constructor
	def __init__(self, path):

		# Normalise path
		path = os.path.normpath(path)
		# Assign attributes value
		self.__path = path
		self.__dirPath, doc = os.path.split( path )
		self.__dirName = os.path.split(self.__dirPath)[1]
		self.__head = []
		self.__tail = []
		self.__number = None
		self.__padding = None		
		body, self.__ext = os.path.splitext(doc)

		self.__numStart = True if reNumStart.match( body ) else False
		self.__numIndex = None
		self.__alphaSubSet = reNonDigits.findall( body )
		self.__numSubSet = reDigits.findall( body )
		self.__create_subsets()


	# Private methods
	def _get_path(self):
		return self.__path

	def _get_dirPath(self):
		return self.__dirPath

	def _get_dirName(self):
		return self.__dirName

	def _get_head(self):
		return self.__head

	def _get_tail(self):
		return self.__tail

	def _get_number(self):
		return self.__number

	def _get_padding(self):
		return self.__padding

	def _get_ext(self):
		return self.__ext

	def _set_readonly(self, value):
		raise TypeError("Read-only attribute")

	# Read-only immutable public attributes
	path = property(_get_path, _set_readonly, doc="Absolute path of the file")
	dirPath = property(_get_dirPath, _set_readonly, doc="Absolute path where the sequence reside")
	dirName = property(_get_dirName, _set_readonly, doc="String of the directory name where the sequence reside")
	head = property(_get_head, _set_readonly, doc="String preceding sequence number")
	tail = property(_get_tail, _set_readonly, doc="String after the sequence number")
	number = property(_get_number, _set_readonly, doc="Integer number of the file within a sequence")
	padding = property(_get_padding, _set_readonly, doc="Integer quantity of integers used to describe the sequence number")
	ext = property(_get_ext, _set_readonly, doc="String representing the extension of the file")


	# Private methods
	def __create_subsets(self):
		tmpNum = list(self.__numSubSet)
		tmpAlpha = list(self.__alphaSubSet)
		subsets = []
		i = 1
		while tmpNum or tmpAlpha:
			if (self.__numStart and i%2) or (not self.__numStart and not i%2):
				subsets.append(tmpNum.pop(0))
			else:
				subsets.append(tmpAlpha.pop(0))
			i+=1
		self.__subsets = list(subsets)



	# Public methods
	def set_num_index(self, ind):
		#Sets the index deciding which numerical part of the name string will be chosen for the numerotation.
		#ex:  "shot50_beauty_v001.0034.png"  and index of 1 would refer to '50' and an index of -1 would refer to '0034'.

		#If numerical component in frame
		if self.__numSubSet:
			#If index is within range of num sub list
			if abs(ind) <= len(self.__numSubSet):
				#format index
				if ind > 0:
					ind -= 1
					unsignedInd = ind
				else:
					unsignedInd = len(self.__numSubSet)+ind
				#assign attributes
				self.__numIndex = ind
				self.__number = int(self.__numSubSet[self.__numIndex])
				self.__padding = len(self.__numSubSet[self.__numIndex])
				#create temps vars
				tmpNum = list(self.__numSubSet)
				tmpAlpha = list(self.__alphaSubSet)
				#Loop through digital and nonDigital parts to create head and tail
				#head
				d = 0
				while unsignedInd >= len(self.__numSubSet)-len(tmpNum) and (tmpAlpha or tmpNum):
					if (self.__numStart and not d%2) or (not self.__numStart and d%2):
						if unsignedInd == len(self.__numSubSet)-len(tmpNum):
							del tmpNum[0]
						else:				
							self.__head.append(tmpNum.pop(0))
					else:
						self.__head.append(tmpAlpha.pop(0))
					d += 1
				#tail
				d = 0
				while tmpAlpha or tmpNum:
					if not d%2:
						self.__tail.append(tmpAlpha.pop(0))
					else:
						self.__tail.append(tmpNum.pop(0))
					d += 1
				return True
		# if no numerical subset
		# or ind is None ( alone without sequence )
		# or ind is out of range

		# put everyting in head
		tmpNum = list(self.__numSubSet)
		tmpAlpha = list(self.__alphaSubSet)
		d = 1
		while tmpAlpha or tmpNum:
			if (self.__numStart and d%2) or (not self.__numStart and not d%2):
				if tmpNum:
					self.__head.append(tmpNum.pop(0))
				else:
					self.__head.append(tmpAlpha.pop(0))
			else:
				if tmpAlpha:
					self.__head.append(tmpAlpha.pop(0))
				else:
					self.__head.append(tmpNum.pop(0))


	def differences(self, fr):
		# Returns the index of the numSubset where there is only one numerical difference
		# If alphaSubset is the same and single difference in numSubset
		# If more than one difference, returns None

		if len(self.__subsets) == len(fr.__subsets):
			if self.__alphaSubSet == fr.__alphaSubSet:
				if len(self.__numSubSet) == len(self.__numSubSet):
					i = 0
					diff = []
					while i < len(self.__numSubSet):
						if self.__numSubSet[i] != fr.__numSubSet[i]:
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
	dir = os.path.normpath( dir )
	files = os.listdir(dir)
	files.sort()
	seq =[]
	if files:
		for f in files:
			p = os.path.join(dir, f)
			if os.path.isfile(p):
				seq.append( Frame( p ) )
		return seq
	else:
		return []

def create_sequences_from_frames( frames, strict_ind = False, ind = -1 ):
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





p = os.path.normpath("P:/Programming/Python/seq/tests")
#p = os.path.normpath("P:/Programming/Python/seq/tests/small")
f = get_frames_from_directory(p)

#print(s[0].__dict__)
#pp.pprint(s[0].__dict__)
s = create_sequences_from_frames(f)
print('LEN: ', len(s) )

for item in s:
	pp.pprint(item.__dict__)
	#print(item.padded_path(), len(item.frames))
	print(" ")
"""
print(s[9])
pp.pprint(s[1].__dict__)
print(s[1].range)
"""