"""
Implementation of custom miner resource
"""
import simpy
import numpy as np
from block import Block
from broadcast import broadcast
from utils import getBlockDelay
from transactionPool import TransactionPool

class Miner:
	"""docstring for Miner"""

	def __init__(self, identifier, env, neighbourList, pipes, miners, location, params):
		self.identifier = identifier
		self.env = env
		self.neighbourList = neighbourList
		self.pipes = pipes
		self.miners = miners
		self.location = location
		self.params = params
		self.transactionPool = TransactionPool(env, identifier, neighbourList, miners, params)
		self.pool = []
		self.block = []
		self.parentQueue = []
		self.blockchain = []
		self.currentBlockID = 0
		self.blockGeneratorAction = self.env.process(self.blockGenerator(params))
		self.env.process(self.receiveBlock())

	def blockGenerator(self, params):
		"""Block generator"""
		while True:
			try:
				delay = getBlockDelay(self.params['blockMu'], self.params['blockSigma'])
				yield self.env.timeout(delay)

				transactionCount = int(params["blockCapacity"])
				transactionList = self.transactionPool.getTransaction(transactionCount)
				l = []
				for transaction in transactionList:
					l.append(transaction.identifier)
				b = Block("B"+str(self.currentBlockID), transactionList, params)
				print("%7.4f" % self.env.now+" : Miner %s proposing %s with transaction list count %d" % (
					self.identifier, b.identifier, len(l)))

				if bool(self.params['verbose']):
					print("%7.4f"%self.env.now+" : Miner %s"%self.identifier+\
								" generated Block %s"%b.identifier)
				self.blockchain.append(b)
				if bool(self.params['verbose']):
					self.displayChain()

				# Broadcast block to all neighbours
				l = []
				for transaction in transactionList:
					l.append(transaction.identifier)
				broadcast(self.env, b, "Block", self.identifier, self.neighbourList, \
							self.params, pipes=self.pipes, miners=self.miners)

				# Remove transactions from local pool
				self.transactionPool.popTransaction(transactionCount)
				self.currentBlockID += 1

			except simpy.Interrupt:
				if bool(self.params['verbose']):
					print("%7.4f"%self.env.now+" : " + "Miner %s"%self.identifier + " interrupted. To mine block %s"%(self.currentBlockID+1) + " now")
				self.currentBlockID += 1

	def validator(self):
		"""Validate transactions"""
		if bool(self.params['verbose']):
			print("miner", self.pipes)

	def getBlockchain(self):
		self.env.timeout(0.5*2)
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
				# Interrupt block generation
				self.blockGeneratorAction.interrupt()

				"""Remove already mined transactions from private pool"""
				for transaction in b.transactionList:
					if transaction in self.transactionPool.transactionList:
						self.transactionPool.transactionList.remove(transaction)
						self.transactionPool.prevTransactions.append(transaction)
				"""Append block to own chain"""
				self.blockchain.append(b)
				if bool(self.params['verbose']):
					print("%7.4f"%self.env.now+" : "+"Miner %s"%self.identifier+\
						" added Block %s"%b.identifier+" to the chain")
					self.displayChain()
			else:
				"""If an invalid block is received, check neighbours and update 
				the chain if a longer chain is found"""
				self.updateBlockchain()
		
	def updateBlockchain(self):
		"""Update blockchain by requesting blocks from peers"""
		maxChain = self.blockchain.copy()
		neighbourID = "-"
		flag = False
		for neighbour in self.neighbourList:
			neighbourChain = self.miners[neighbour].getBlockchain()
			if len(maxChain) < len(neighbourChain):
				maxChain = neighbourChain.copy()
				neighbourID = neighbour
				flag = True
		self.blockchain = maxChain.copy()
		if flag:
			self.currentBlockID = int(self.blockchain[-1].identifier[1:])+1
		if bool(self.params['verbose']):
			print("%7.4f"%self.env.now+" : "+"Miner %s"%self.identifier+\
			" updated to chain of %s with latest block %s"%(neighbourID, block.identifier))

	def displayChain(self):
		chain = [b.identifier for b in self.blockchain]
		print("%7.4f"%self.env.now+" : Miner %s"%self.identifier+\
					" has current chain: %s"%chain)
	
	def displayLastBlock(self):
		if self.blockchain:
			block = self.blockchain[-1]
			transactions = block.transactionList
		print("%7.4f"%self.env.now+" : Miner %s"%self.identifier+\
                    " has last block: %s" % transactions)
