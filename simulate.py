import simpy
import numpy as np
from block import Block
from network import Network

def simulate(env, params):
	"""Begin simulation"""
	net = Network("Blockchain", env, params)
	net.addPipes(params['numMiners'])
	net.addMiners(params['numMiners'])

env = simpy.Environment()

params = {}
params['mu'] = 10
params['sigma'] = 5
params['numMiners'] = 2
params['simulationTime'] = 100

simulate(env, params)

env.run(until = params['simulationTime'])