"""
TODO : Implementation of custom miner resource
- maintain Parent Queue
- maintain Transaction pool
- implement chain updation
"""
import simpy
import numpy as np
from block import Block
class Miner:
	"""docstring for Miner"""
	def __init__(self, identifier, env, transactionPool, neighbourList, pipes, params):
		self.identifier = identifier
		self.env = env
		self.neighbourList = neighbourList
		self.pipes = pipes
		self.params = params
		self.transactionPool = transactionPool
		self.pool = []
		self.block = []
		self.parentQueue = []
		self.blockchain = []
		self.env.process(self.blockGenerator(params))
		self.env.process(self.receiveBlock())

	def blockGenerator(self, params):
		"""Block generator"""
		transactionCount = min(int(params["blockCapacity"]), len(self.transactionPool))
		transactionList = self.transactionPool[:transactionCount]

		blockID = 0
		while True:
			b = Block(blockID, transactionList, params)
			delay = (self.params['mu']+self.params['sigma']*np.random.\
												randn(1))[0]
			yield self.env.timeout(delay)
			if bool(self.params['verbose']):
				print("%7.4f"%self.env.now+" : Miner%d"%self.identifier+\
							" generated Block%d"%blockID)
			self.blockchain.append(b)
			self.broadcastBlock(b)
			blockID += 1

	def validator(self):
		"""Validate transactions"""
		if bool(self.params['verbose']):
			print("miner", self.pipes)

	def broadcastBlock(self, block):
		"""Broadcast a block to all neighbours"""
		if not self.pipes:
			raise RuntimeError('There are no output pipes.')
		events = []
		for neighbourID in self.neighbourList:
			store = self.pipes[neighbourID]
			events.append(store.put(block, self.identifier))

		if bool(self.params['verbose']):
			print("%7.4f"%self.env.now+" : "+"Miner%d propagated Block%d"%\
					(self.identifier, block.identifier))
		print(events)
		return self.env.all_of(events)  # Condition event for all "events"

	def receiveBlock(self):
		"""Receive newly mined block from neighbour"""
		while True:
			b = yield self.pipes[self.identifier].get()
			if len(self.blockchain) > 0:
				currID = self.blockchain[-1].identifier
			else:
				currID = -1
			if b.identifier <= currID:
				pass
				if bool(self.params['verbose']):
					print("%7.4f"%self.env.now+" : "+"Miner%d"%self.identifier+\
						" received previous Block%d"%b.identifier)
			elif b.identifier == currID+1:
				self.blockchain.append(b) # to shift to appropriate condition below
				if bool(self.params['verbose']):
					print("%7.4f"%self.env.now+" : "+"Miner%d"%self.identifier+\
						" added Block%d"%b.identifier+" to the chain")
			else:
				self.updateBlockchain(b)
		
	def updateBlockchain(self, block):
		"""Update blockchain by requesting blocks from peers"""
		if bool(self.params['verbose']):
			print("%7.4f"%self.env.now+" : "+"Miner%d"%self.identifier+\
				" updated to Block%d"%block.identifier)
		pass
