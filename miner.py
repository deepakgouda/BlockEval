class Miner:
	"""docstring for Miner"""
	def __init__(self, id, env):
		self.id = id
		self.env = env
		self.action = self.env.process(blockGenerator(name, blockParams))
		self.pool = []
		self.block = []

	def blockGenerator(name, blockParams):
		"""Block generator"""
		b = Block(name, blockParams)
		# return b
		env.timeout(blockParams['delay'])
		print("%7.4f"%env.now+" : "+"Block generated")
		yield b

	def validator():
		"""Validate transactions"""
		pass

	def propagate(self):
		"""Propagate block to network"""
		print("%7.4f"%self.env.now+" : "+"Block propagated")
