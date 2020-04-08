"""
Implementation of custom full node resource
"""
import simpy
import numpy as np
from block import Block
from broadcast import broadcast
from utils import getBlockDelay, getTransmissionDelay
from transactionPool import TransactionPool

class FullNode:
	"""docstring for FullNode"""

	def __init__(self, identifier, env, neighbourList, pipes, nodes, location, params):
		self.identifier = identifier
		self.env = env
		self.neighbourList = neighbourList
		self.pipes = pipes
		self.nodes = nodes
		self.location = location
		self.params = params
		self.transactionPool = TransactionPool(env, identifier, neighbourList, nodes, params)
		self.pool = []
		self.block = []
		self.parentQueue = []
		self.blockchain = []
		self.currentBlockID = 0
		self.env.process(self.receiveBlock())

	def validator(self):
		"""Validate transactions"""
		if bool(self.params['verbose']):
			print("miner", self.pipes)

	def getBlockchain(self, destination):
		self.env.timeout(getTransmissionDelay(self.location, destination)*2)
		return self.blockchain

	def receiveBlock(self):
		"""Receive newly mined block from neighbour"""
		while True:
			b = yield self.pipes[self.identifier].get()
			if len(self.blockchain) > 0:
				currID = int(self.blockchain[-1].identifier[1:])
			else:
				currID = -1
			currIDs = [x.identifier for x in self.blockchain]
			if int(b.identifier[1:]) == currID+1 and b.identifier not in currIDs:

				"""Remove already mined transactions from private pool"""
				for transaction in b.transactionList:
					if transaction in self.transactionPool.transactionList:
						self.transactionPool.transactionList.remove(transaction)
						self.transactionPool.prevTransactions.append(transaction)
				"""Append block to own chain"""
				self.blockchain.append(b)
				if bool(self.params['verbose']):
					print("%7.4f"%self.env.now+" : "+"%s"%self.identifier+\
						" added Block %s"%b.identifier+" to the chain")
					self.displayChain()
			else:
				"""If an invalid block is received, check neighbours and update 
				the chain if a longer chain is found"""
				self.updateBlockchain()
		
	def updateBlockchain(self):
		"""Update blockchain by requesting blocks from peers"""
		maxChain = self.blockchain.copy()
		neighbourID = ""
		flag = False
		for neighbour in self.neighbourList:
			neighbourChain = self.nodes[neighbour].getBlockchain(self.location)
			if len(maxChain) < len(neighbourChain):
				maxChain = neighbourChain.copy()
				neighbourID = neighbour
				flag = True
		self.blockchain = maxChain.copy()
		if flag:
			self.currentBlockID = int(self.blockchain[-1].identifier[1:])+1
		if bool(self.params['verbose']):
			if neighbourID:
				print("%7.4f"%self.env.now+" : "+"%s"%self.identifier+\
					" updated to chain of %s"%(neighbourID))

	def displayChain(self):
		chain = [b.identifier for b in self.blockchain]
		print("%7.4f"%self.env.now+" : %s"%self.identifier+\
					" has current chain: %s"%chain)
	
	def displayLastBlock(self):
		if self.blockchain:
			block = self.blockchain[-1]
			transactions = block.transactionList
		print("%7.4f"%self.env.now+" : %s"%self.identifier+\
                    " has last block: %s" % transactions)
