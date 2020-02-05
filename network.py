import simpy
import numpy as np
from miner import Miner
from block import Block
from pipe import Pipe
from broadcast import broadcast
from transaction import Transaction
from utils import getTransmissionDelay

class Network:
	"""docstring for Network"""
	def __init__(self, name, env, params):
		self.name = name
		self.env = env
		self.params = params
		self.locations = params['locations']
		self.miners = {}
		self.pipes = {}
		self.env.process(self.addTransaction())

	def addMiners(self, numMiners):
		"""Add miner to network"""
		for identifier in range(numMiners):
			neighbourList = ["M%d"%x for x in list(range(identifier)) + list(range(identifier+1, numMiners))] 
			location = np.random.choice(self.locations, size=1)[0]
			self.miners["M%d"%identifier] = Miner("M%d"%identifier, self.env,\
										neighbourList, self.pipes, self.miners, location, self.params)
			if bool(self.params['verbose']):
				print("%7.4f"%self.env.now+" : "+"Miner added at location %s"%location)

	def addPipes(self, numMiners):
		for identifier in range(numMiners):
			self.pipes["M%d"%identifier] = Pipe(self.env, "M%d"%identifier)

	def addTransaction(self):
			num = 0
			while True:
				source = np.random.choice(self.locations, size=1)[0]
				destination = np.random.choice(self.locations, size=1)[0]
				delay = getTransmissionDelay(source, destination)
				yield self.env.timeout(delay)
				transaction = (Transaction("T%d"%num, self.env.now))
				if bool(self.params['verbose']):
						print("%7.4f" % self.env.now+" : " +"%s added" % (transaction.identifier))
				# Broadcast transactions to all neighbours
				broadcast(self.env, transaction, "Transaction", "TempID", \
					['M0', 'M2'], self.params, miners=self.miners)
				num+=1
	
	def displayChains(self):
		print("\n--------------------All Miners--------------------\n")
		for miner in self.miners.values():
			miner.displayChain()

