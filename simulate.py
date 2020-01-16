import simpy
import numpy as np
from block import Block
from network import Network

def simulate(env, params):
	"""Begin simulation"""
	net = Network("Blockchain", env, params)
	net.addMiner(params['numMiners'])

env = simpy.Environment()

params = {}
params['mu'] = 10
params['sigma'] = 1
params['numMiners'] = 2

simulate(env, params)

env.run(until = 100)