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
		# Degree of network graph. Degree >= n/2 guarantees a connected graph
		degree = numMiners//2 + 1
		for identifier in range(numMiners):
			# Possible neighbours are [0, 1, ... i-1, i+1, ... n]
			possibleNeighbours = list(range(identifier)) + \
                    	list(range(identifier+1, numMiners))
			# Generate a random sample of size degree without replacement from possible neighbours
			randNeighbour = np.random.choice(possibleNeighbours, size=degree, replace=False)
			neighbourList = ["M%d"%x for x in randNeighbour]
			# self.miners["M%d"%identifier] = Miner("M%d"%identifier, self.env,\
			# 							neighbourList, self.pipes, self.miners, self.params)
			# if bool(self.params['verbose']):
			# 	print("%7.4f" % self.env.now+" : "+"%s added with neighbourList %s" %
			# 		("M%d" % identifier, neighbourList))
			# neighbourList = ["M%d"%x for x in list(range(identifier)) + list(range(identifier+1, numMiners))] 
			location = np.random.choice(self.locations, size=1)[0]
			self.miners["M%d"%identifier] = Miner("M%d"%identifier, self.env,\
										neighbourList, self.pipes, self.miners, location, self.params)
			if bool(self.params['verbose']):
				print("%7.4f"%self.env.now+" : "+"%s added at location %s with neighbour list %s"%("M%d"%identifier, location, neighbourList))

	def addPipes(self, numMiners):
		for identifier in range(numMiners):
			self.pipes["M%d"%identifier] = Pipe(self.env, "M%d"%identifier, self.miners)

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

