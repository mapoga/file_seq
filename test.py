import os

path = r"P:\Programming\Python\seq\scripts\file_seq\tests\small"
print(path)

w = [[dirpath, dirnames, filenames] for dirpath, dirnames, filenames in os.walk(path)][0]
print(w)[2][-1:]