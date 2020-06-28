import simpy
import string
import random

def getHash(k):
	return ''.join(random.choices(string.ascii_lowercase+string.digits, k=k))

class Block:
	"""docstring for Block"""
	def __init__(self, identifier, transactionList, params, size, type):
		self.params = params
		self.identifier = identifier
		self.transactionList = transactionList
		self.hash = self.identifier+"_"+getHash(10)
		self.size = size
		self.type = type
