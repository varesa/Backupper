#!/opt/python3/bin/python3

# IMPORTS
import sys
import os

import Debug
# IMPORTS END


# ALIASES
msg = Debug.msg
# ALIASES END


# SETTINGS
Debug.setenabled(True)
# SETTINGS END


# GLOBALS
cf = None # Files to store configuration and rotations
rf = None

dir = None # Path to this script

preferences = {'history_size' : 10} # Default preferences, will be overwritten by config
# GLOBALS END 


# FUNCTIONS
def getpath():
	global dir
	dir=sys.path[0]
	Debug.msg("Directory is: " + dir + "\n")


def openconfigurationfile():	# Opens a file handle to rotationFile
	global cf
	global dir
	cf = open(dir + os.sep + 'preferences',mode='r+',encoding='utf-8')

def readconfiguration():
	global cf
	global preferences
	
	for line in cf:
		Debug.msg("Configuration line: " + line.rstrip())
		
		if line[0] == '#':
			continue
			
		key = line.partition(':')[0]
		rhs = line.partition(':')[2]
		value = rhs.partition('#')[0]
		
		if key == 'history_size':
				if int(value) > 0 or int(value) < 1000:
					preferences['history_size'] = value 
				else:
					sys.exit("Invalid valure after: history_size")
		
		print("")	# Newline		
		

def closeconfigurationfile(): # Closes the file handle to rotationFile
	global cf
	cf.close()

def printconfiguration():
	global preferences
	Debug.msg("Preferences:")
	for pref, value in preferences.items():
		print(pref + ": " + value.rstrip());
	print("")	# Newline

	
def openrotationfile():	# Opens a file handle to rotationFile
	global rf
	rf = open(dir + os.sep + 'rotation',mode='r+',encoding='utf-8')

def getnumofrecords():
	global rf
	if(rf != None):
		Debug.msg("Number of records: " + str( len( rf.readlines() ) ) + "\n" )
	else:
		print("RotationFile is not open!")

def closerotationfile(): # Closes the file handle to rotationFile
	global rf
	rf.close()
# FUNCTIONS END

# MAIN
getpath()

openconfigurationfile()		# Get configuration
readconfiguration()
closeconfigurationfile()
printconfiguration()

openrotationfile()
getnumofrecords()
closerotationfile()
# MAIN END
