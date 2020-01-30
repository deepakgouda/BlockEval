import simpy
import numpy as np
from miner import Miner
from block import Block
from pipe import Pipe
from broadcast import broadcast
from transaction import Transaction

class Network:
	"""docstring for Network"""
	def __init__(self, name, env, params):
		self.name = name
		self.env = env
		self.params = params
		self.miners = {}
		self.pipes = {}
		self.env.process(self.addTransaction())

	def addMiners(self, numMiners):
		"""Add miner to network"""
		for identifier in range(numMiners):
			neighbourList = ["M%d"%x for x in list(range(identifier)) + list(range(identifier+1, numMiners))] 
			self.miners["M%d"%identifier] = Miner("M%d"%identifier, self.env,\
																			neighbourList, self.pipes, self.miners, self.params)
			if bool(self.params['verbose']):
				print("%7.4f"%self.env.now+" : "+"Miner added")

	def addPipes(self, numMiners, capacity=simpy.core.Infinity):
		for identifier in range(numMiners):
			self.pipes["M%d"%identifier] = Pipe(self.env, "M%d"%identifier)

	def addTransaction(self):
			num = 0
			while True:
					delay = (self.params['transactionMu']+self.params['transactionSigma']*np.random.randn(1))[0]
					yield self.env.timeout(delay)
					transaction = (Transaction("T%d"%num, self.env.now))
					if bool(self.params['verbose']):
							print("%7.4f" % self.env.now+" : " +"%s added" % (transaction.identifier))
					# Broadcast transactions to all neighbours
					broadcast(self.env, transaction, "Transaction", "TempID", \
											["M0", "M1"], self.params, miners=self.miners)
					num+=1
