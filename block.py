import simpy

class Block:
	"""docstring for Block"""
	def __init__(self, identifier, transactionList, params):
		self.params = params
		self.identifier = identifier
		self.transactionList = transactionList
