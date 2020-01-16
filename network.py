import simpy
import numpy as np
from block import Block
from transaction import Transaction

class Network:
	"""docstring for Network"""
	def __init__(self, name, env, params):
		self.name = name
		self.env = env
		self.params = params
		self.transactionList=[]
		self.miner = []
		self.env.process(self.addTransaction())
		self.env.process(self.main())

	def addMiner(self, numMiners):
		"""Add miner to network"""
		self.miner = simpy.Resource(self.env, capacity=\
												numMiners)
		print("%7.4f"%self.env.now+" : "+"Miner added")

	def addTransaction(self):
		"""Generate transactions in network"""
		num=0
		while True:
			print("%7.4f"%self.env.now+" : "+\
							"Transaction%d added"%num)
			self.transactionList.append(Transaction(\
							"Transaction%d"%num, self.env.now))
			delay = (self.params['mu']+self.params['sigma']*np.random.\
												randn(1))[0]
			yield self.env.timeout(delay)
			num+=1
			if num == 5:
				return

	def main(self):
		"""Transactions request resource i.e. miner and wait 
		for confirmation or fail"""
		while True:
			while len(self.transactionList) > 0:
				transaction = self.transactionList.pop(0)
				print("%7.4f"%self.env.now+" : "+\
							"%s evaluating"%\
							transaction.identifier)
				with self.miner.request() as req:
					arrive = self.env.now
					patience = np.random.uniform(0, 10)
					results = yield req | self.env.timeout(patience)
					wait = self.env.now-arrive
					if req in results:
						# We got the miner
						confirmation = (self.params['mu']+self.params\
								['sigma']*np.random.randn(1))[0]
						yield self.env.timeout(confirmation)
						print("%7.4f"%self.env.now+" : "+\
									"%s confirmed"\
									%transaction.identifier)
					else:
						# No confirmation
						print("%7.4f"%self.env.now+" : "+\
									"%s failed"\
									%transaction.identifier)
			yield self.env.timeout(1)
				
