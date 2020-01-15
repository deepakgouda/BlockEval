class Network:
	"""docstring for Network"""
	def __init__(self, name):
		self.name = name

	def addBlock(self, block):
		"""Add block to network"""
		print(block.name+" added")

	def propagate(self):
		"""Propagate block to network"""
		print("Block propagated")

		