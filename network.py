import simpy
from block import Block

class Network:
	"""docstring for Network"""
	def __init__(self, name, env, blockParams):
		self.name = name
		self.env = env

	def addBlock(self, block):
		"""Add block to network"""
		print("%7.4f"%self.env.now+" : "+block.name+" added")

	def addMiner(self, numMiners):
		"""Add miner to network"""
		self.miner = simpy.Resource(self.env, capacity = numMiners)
		print("%7.4f"%self.env.now+" : "+"Miner added")

	def addTransaction(self, params):
		"""Generate transactions in network"""
		print("%7.4f"%self.env.now+" : "+"Transaction added")


		