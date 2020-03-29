import simpy
import numpy as np
import json
from block import Block
from network import Network
from time import time

def simulate(env, params):
	"""Begin simulation"""
	net = Network("Blockchain", env, params)
	net.addNodes(params['numMiners'], params['numFullNodes'])
	net.addPipes(params['numMiners'], params['numFullNodes'])
	return net

# Load parameters from params.json
with open('params.json', 'r') as f:
	params = f.read()
params = json.loads(params)

np.random.seed(7)
env = simpy.Environment()
net = simulate(env, params)
env.run(until = params['simulationTime'])
net.displayChains()
