import simpy
import numpy as np
from miner import Miner
from block import Block
from transaction import Transaction
from pipe import Pipe

class Network:
	"""docstring for Network"""
	def __init__(self, name, env, params):
		self.name = name
		self.env = env
		self.params = params
		self.transactionPool=[]
		self.miners = []
		self.pipes = []
		# self.env.process(self.addTransaction())

	def addMiners(self, numMiners):
		"""Add miner to network"""
		for identifier in range(numMiners):
			neighbourList = list(range(identifier)) + list(range(identifier+1, numMiners))
			self.miners.append(Miner(identifier, self.env, self.transactionPool, \
								neighbourList, self.pipes, self.miners, self.params))
			if bool(self.params['verbose']):
				print("%7.4f"%self.env.now+" : "+"Miner added")

	def addPipes(self, numMiners, capacity=simpy.core.Infinity):
		for identifier in range(numMiners):
			self.pipes.append(Pipe(self.env, identifier))

	def addTransaction(self):
		"""Generate transactions in network"""
		num=0
		while True:
			if bool(self.params['verbose']):
				print("%7.4f"%self.env.now+" : "+\
						"Transaction%d added"%num)
			self.transactionPool.append(Transaction(\
							"Transaction%d"%num, self.env.now))
			delay = (self.params['mu']+self.params['sigma']*np.random.\
												randn(1))[0]
			yield self.env.timeout(delay)
