import simpy
import numpy as np
from miner import Miner
from fullNode import FullNode
from block import Block
from pipe import Pipe
from broadcast import broadcast
from transaction import Transaction
from utils import getTransactionDelay

class Network:
	"""docstring for Network"""
	def __init__(self, name, env, params):
		self.name = name
		self.env = env
		self.params = params
		self.locations = params['locations']
		self.miners = {}
		self.fullNodes = {}
		self.nodes = {}
		self.pipes = {}
		self.env.process(self.addTransaction())

	def addNodes(self, numMiners, numFullNodes):
		"""Add Nodes to network"""
		numNodes = numFullNodes + numMiners
		# Degree of network graph. Degree >= n/2 guarantees a connected graph
		degree = numNodes//2 + 1
		for identifier in range(numNodes):
			# Possible neighbours are [0, 1, ... i-1, i+1, ... n]
			possibleNeighbours = list(range(identifier)) + \
                    	list(range(identifier+1, numNodes))
			# Generate a random sample of size degree without replacement from possible neighbours
			randNeighbour = np.random.choice(possibleNeighbours, size=degree, replace=False)
			neighbourList = ["M%d"%x if x < numMiners else "F%d"%(x-numMiners) for x in randNeighbour]

			location = np.random.choice(self.locations, size=1)[0]
			if identifier < numMiners:
				self.miners["M%d"%identifier] = Miner("M%d"%identifier, self.env,\
											neighbourList, self.pipes, self.nodes, location, self.params)
				if bool(self.params['verbose']):
					print("%7.4f"%self.env.now+" : "+"%s added at location %s with neighbour list %s" % 
						("M%d"%identifier, location, neighbourList))
			else:
				self.fullNodes["F%d" % (identifier-numMiners)] = FullNode("F%d" % (identifier-numMiners), self.env,
											neighbourList, self.pipes, self.nodes, location, self.params)
				if bool(self.params['verbose']):
					print("%7.4f" % self.env.now+" : "+"%s added at location %s with neighbour list %s" %
						("F%d" % identifier, location, neighbourList))
		self.nodes.update(self.miners)
		self.nodes.update(self.fullNodes)

	def addPipes(self, numMiners, numFullNodes):
		for identifier in range(numMiners):
			self.pipes["M%d"%identifier] = Pipe(self.env, "M%d"%identifier, self.nodes)
		for identifier in range(numFullNodes):
			self.pipes["F%d"%identifier] = Pipe(self.env, "F%d"%identifier, self.nodes)

	def addTransaction(self):
			num = 0
			while True:
				# source = np.random.choice(self.locations, size=1)[0]
				# destination = np.random.choice(self.locations, size=1)[0]
				# delay = getTransmissionDelay(source, destination)
				delay = getTransactionDelay(
					self.params['transactionMu'], self.params['transactionSigma'])
				yield self.env.timeout(delay)
				transaction = (Transaction("T%d"%num, self.env.now))
				if bool(self.params['verbose']):
						print("%7.4f" % self.env.now+" : " +"%s added" % (transaction.identifier))
				"""Broadcast transactions to all neighbours"""
				transactionNeighbours = list(np.random.choice(list(self.nodes.keys()), size=len(self.nodes)//2))
				broadcast(self.env, transaction, "Transaction", "TempID", \
					transactionNeighbours, self.params, nodes=self.nodes)
				num+=1
	
	def displayChains(self):
		print("\n--------------------All Miners--------------------\n")
		for node in self.nodes.values():
			node.displayChain()

