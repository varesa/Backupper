import sys

enabled=False;

def setenabled(bool):	# Toggles debugging messages
	global enabled
	if bool==True:
		enabled=True
	elif bool==False:
		enabled=False
	else:
		sys.exit("Error: Please specify a boolean argument")
		
def msg(msg):			# Easily removable debugging messages
	global enabled
	if enabled:
		print(msg)
