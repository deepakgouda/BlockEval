import simpy
import numpy as np
from block import Block
from network import Network

def generateTransactions(net, params):
	"""Transaction generator"""
	delay = 3
	net.addTransaction(params)
	yield env.timeout(delay)

def simulate(net, env, params):
	"""Begin simulation"""
	# blist = []
	# for i in range(1, 6):
	# 	delay = params['mu']+params['sigma']*np.random.randn()
		# b = blockGenerator("Block%d"%i, net.miner, params)
		# blist.append(b)
		# b.validate(env, net.miner, delay)
		# print("%7.4f"%env.now+" : "+b.name+" started validation at %7.4f"%env.now)
		# yield env.timeout(delay)
		# print("%7.4f"%env.now+" : "+b.name+" validated at %7.4f"%env.now)
		# net.addBlock(b)
		# net.propagate()
	pass

env = simpy.Environment()
numMiners = 2
params = {}
params['mu'] = 10
params['sigma'] = 1
net = Network("Net1", env)
net.addMiner(numMiners)
# net.addTransactionGenerator()
env.process(generateTransactions(net, params))
env.process(simulate(net, env, params))
env.run(until = 30)