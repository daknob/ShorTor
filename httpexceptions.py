#!bin/python

class BadInputException(Exception):
	def __init__(self, errormsg, statuscode):
		self.errormsg = errormsg
		self.statuscode = statuscode
	def getError(self):
		return self.errormsg
	def getCode(self):
		return self.statuscode

if (__name__ == "__main__"):
	exit(0)
