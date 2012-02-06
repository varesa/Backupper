#!/opt/python3/bin/python3

from sys import path
from os import sep
from subprocess import call
from time import strftime,sleep
from pickle import dump,load

import Debug

# ALIASES
msg = Debug.msg

# SETTINGS
Debug.setenabled(False)

# GLOBALS
cf = None # Files to store configuration and rotations
rf = None

records = None # List to hold all backup-records

dir = None # Path to this script

preferences = {'history_size' : 10} # Default preferences, will be overwritten by config

# FUNCTIONS
def getpath():
	global dir
	dir=path[0]	#sys.path
	Debug.msg("Directory is: " + dir + "\n")

def openconfigurationfile():	# Opens a file handle to rotationFile
	global cf
	global dir
	cf = open(dir + sep + 'preferences',mode='r+',encoding='utf-8') # sep -> os.sep

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
		Debug.msg("")	# Newline		

def closeconfigurationfile(): # Closes the file handle to rotationFile
	global cf
	cf.close()

def printconfiguration():
	global preferences
	Debug.msg("Preferences:")
	for pref, value in preferences.items():
		Debug.msg(pref + ": " + value.rstrip())
	Debug.msg("")	# Newline

def openrotationfile():	# Opens a file handle to rotationFile
	global rf
	rf = open(dir + sep + 'rotation',mode='rb+') # sep -> os.sep

def getrecords():
	global rf
	global records
	records = load(rf) # load -> pickle.load
	Debug.msg("Number of records: " + str( len(records) ) + "\n" )

def backup():
	global dir
	global records
	time=strftime("%Y.%m.%d_%H-%M-%S")
	call(['mkdir', dir + sep + 'testenv' + sep + time])
	call(['rsync', '-va', '--delete', '--link-dest=' + dir + sep + 'testenv' + sep + records[len(records)-2], dir + sep + 'testenv/data', dir + sep + 'testenv/' + time + sep]) # sep -> os.sep
	records.append(time)

def removeolds():
	global records
	global preferences
	while len(records) > int(preferences['history_size']):
		call(['rm', "testenv/" + records[0], '-R'])
		records.pop(0)
	
def rewriterecords():
	global rf
	global records
	rf.seek(0)
	dump(records,rf) # dump .> pickle.dump
	

def closerotationfile(): # Closes the file handle to rotationFile
	global rf
	rf.flush()
	rf.close()

# MAIN
getpath()

openconfigurationfile()		# Get configuration
readconfiguration()
closeconfigurationfile()
printconfiguration()

openrotationfile()
getrecords()
backup()
removeolds()
rewriterecords()
closerotationfile()

print("\n\n")