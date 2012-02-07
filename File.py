#/opt/python3/bin/python3

def exists(fname):
	file_exists = True
	try:
		f = open(fname, mode="r")
	except IOError:
		file_exists = False
	if file_exists:
		f.close()
		return True
	else:
		return False
