"""
TODO : Implementation of custom miner resource
- maintain Parent Queue
- implement chain updation
- shift delay to a util function
"""
import simpy
import numpy as np
from block import Block
from broadcast import broadcast
from transactionPool import TransactionPool

class Miner:
	"""docstring for Miner"""
	def __init__(self, identifier, env, neighbourList, pipes, miners, params):
		self.identifier = identifier
		self.env = env
		self.neighbourList = neighbourList
		self.pipes = pipes
		self.miners = miners
		self.params = params
		self.transactionPool = TransactionPool(self.env, [0, 1], \
								"T"+str(self.identifier), self.miners, self.params)
		self.pool = []
		self.block = []
		self.parentQueue = []
		self.blockchain = []
		self.currentBlockID = 0
		self.blockGeneratorAction = self.env.process(self.blockGenerator(params))
		self.env.process(self.receiveBlock())

	def blockGenerator(self, params):
		"""Block generator"""
		transactionCount = int(params["blockCapacity"])
		transactionList = self.transactionPool.getTransaction(transactionCount)

		while True:
			try:
				b = Block(self.currentBlockID, transactionList, params)
				delay = (self.params['mu']+self.params['sigma']*np.random.\
													randn(1))[0]
				yield self.env.timeout(delay)
				if bool(self.params['verbose']):
					print("%7.4f"%self.env.now+" : Miner%d"%self.identifier+\
								" generated Block%d"%self.currentBlockID)
				self.blockchain.append(b)
				if bool(self.params['verbose']):
					self.displayChain()
					# self.displayLastBlock()
				# Broadcast block to all neighbours
				broadcast(self.env, b, "Block", self.identifier, self.neighbourList, \
							self.params, pipes=self.pipes)
				
				# Broadcast interrupt to all neighbours
				broadcast(self.env, "", "Interrupt", self.identifier, self.neighbourList,
							self.params, pipes=self.pipes, miners=self.miners)

				self.currentBlockID += 1

			except simpy.Interrupt:
				if bool(self.params['verbose']):
					print("%7.4f"%self.env.now+" : " + "Miner %d"%self.identifier + " interrupted. To mine block %d"%(self.currentBlockID+1) + " now")
				self.currentBlockID += 1

	def validator(self):
		"""Validate transactions"""
		if bool(self.params['verbose']):
			print("miner", self.pipes)

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
					self.displayChain()
					# self.displayLastBlock()
			else:
				self.updateBlockchain(b)
		
	def updateBlockchain(self, block):
		"""Update blockchain by requesting blocks from peers"""
		if bool(self.params['verbose']):
			print("%7.4f"%self.env.now+" : "+"Miner%d"%self.identifier+\
				" updated to Block%d"%block.identifier)
		pass

	def displayChain(self):
		chain = [b.identifier for b in self.blockchain]
		print("%7.4f"%self.env.now+" : Miner%d"%self.identifier+\
					" has current chain: %s"%chain)
	
	def displayLastBlock(self):
		if self.blockchain:
			block = self.blockchain[-1]
			transactions = block.transactionList
		print("%7.4f"%self.env.now+" : Miner%d"%self.identifier+\
                    " has last block: %s" % transactions)
