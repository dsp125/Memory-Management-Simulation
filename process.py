'''
File: process.py 
Author(s): Clarisse Baes, Dhruv Patel, Michael Savini
RPI ID: baesc, pateld7, savinm
PROCESS CLASS DEFINITION for use with project2.py
'''

##PROCESS CLASS DEFINITION
class Process(object):
	def __init__(self):
		self.name = ""			#Stores the name of the process
		self.active = False		#True if process running, False otherwise
		self.complete = False		#True if process done, False otherwise
		self.size = 0			#Stores the size of the process
		self.countComplete = 0		#Completed bursts
		self.start = 0		#Stores the current start time of the process
		self.arrTimes = []		#Stores process burst arrival times
		self.endTimes = []		#Stores process burst end times
