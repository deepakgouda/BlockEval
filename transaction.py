class Transaction:
	"""docstring for Transaction"""
	def __init__(self, identifier, creationTime):
		self.identifier = identifier
		self.creationTime = creationTime

	def display(self):
		print(self.identifier)
		