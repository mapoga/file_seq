f={
	"pad": 4,
	"number": -6,
	"pad1": 4,
	"number1": -6,
	"pad2": 4,
	"number2": -6,
	"pad3": 4,
	"number3": -6,
	"pad4": 4,
	"number4": -6,
	}
s = '{number:#=-{pad}d}'.format(**f)
print(s)

def func():
	return f

print( '{number:#=-{pad}d}'.format(**func()) )
try:
	print( "{0}{1}{2}".format("{", "lol", "}") )
except:
	pass
print(range(1,6))

for key, value in func().items():
	print(key, value)

def lol(first, *args):
	print(first)
	print(args)

lol(1,[2,3])