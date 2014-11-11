import re

class Sequence:

	def __init__(self, data):
		self.sequence = data

	def __repr__(self):
		return "<sequence: {0}>".format(self.sequence)

	def __iter__(self):
		return iter(self.sequence)

	def __getitem__(self, index):
		return self.sequence[index]

	def __delitem__(self, index):
		self.sequence.pop(index)

	def __len__(self):
		return len(self.sequence)

	def __as_list(self):
		data = list(set([ i.number for i in self.sequence ]))
		data.sort()
		return data


	def append(self):
		pass
	def extend(self):
		pass



def sequence_to_range( numbers=[] ): #String
	'''
	Takes a list of numbers as argument and returns a string of the compressed range
	1,4-6,10,15-18,20-26x2,27,28,30-50x5,56,63-72x3
	'''
	try:
		for n in numbers:
			int(n)
	except ValueError:
		raise ValueError("Sequence must contain numbers")
	except TypeError:
		raise TypeError("Sequence must be a list")
	numbers = list(set(numbers))
	numbers.sort()
	stacks = []
	lastStep = 0

	def format_ruled_sequence(seq):
		"""
		Converts a range into "N-NxN" format
		"""
		if len(seq) < 2:
			return "{0}".format(seq[0])
		else:
			step = seq[1]-seq[0]
			if step ==1:
				return "{0}-{1}".format(seq[0], seq[-1])
			else:
				return "{0}-{1}x{2}".format(seq[0], seq[-1], step)

	if numbers:
		# stack sub-sequences in individual list
		for i, n in enumerate(numbers):
			if i == 0:
				#First number, create a stack
				stacks.append([n])
			else:
				# get step from back and front
				back = numbers[i]-numbers[i-1]
				if i != len(numbers)-1:
					front = numbers[i+1]-numbers[i]
				else:
					front = 0

				if back == lastStep:
					stacks[-1].append(n)
				elif front == back:
					if len(stacks[-1]) < 2:
						lastStep = back
						stacks[-1].append(n)
					else:
						lastStep = back
						stacks.append([n])
				else:
					lastStep = back
					stacks.append([n])

		return ','.join(format_ruled_sequence(e) for e in stacks)
	return ""









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
	ls = [1,2,3,4,5,6,8,10,12,14,16,17,19,20,22,25,28,29,31]
	print(ls)
	#print("")
	print(sequence_to_range(ls))
	print("")
	l = [4,8,12,16,17,18,22]
	print(l)
	print(sequence_to_range(l))