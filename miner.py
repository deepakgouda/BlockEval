"""
TODO : Implementation of custom miner resource

- Use Store to queue messages for miner
- maintain Parent Queue
- maintain Transaction pool
- implement broadcast pipeline
- impelment chain updation
"""
import simpy
class Miner:
	"""docstring for Miner"""
	def __init__(self, identifier, env, capacity=simpy.core.Infinity):
		self.identifier = identifier
		self.env = env
		self.action = self.env.process(blockGenerator(name, \
												blockParams))
		self.capacity = capacity
		self.pool = []
		self.block = []
		self.parentQueue = []
		self.pipe = simpy.Store(self.env, capacity=self.capacity)

	def blockGenerator(self, name, blockParams):
		"""Block generator"""
		while True:
			b = Block(name, blockParams)
			env.timeout(blockParams['delay'])
			print("%7.4f"%env.now+" : "+"Block generated")
			yield b

	def validator(self):
		"""Validate transactions"""
		pass

	def propagate(self, block):
		"""Propagate block to network"""
		self.put(block)
		print("%7.4f"%self.env.now+" : "+"Block propagated")
