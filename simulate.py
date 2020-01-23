import simpy
import numpy as np
import json
from block import Block
from network import Network
from time import time

def simulate(env, params):
	"""Begin simulation"""
	net = Network("Blockchain", env, params)
	net.addPipes(params['numMiners'])
	net.addMiners(params['numMiners'])

# Load parameters from params.json
with open('params.json', 'r') as f:
	params = f.read()
params = json.loads(params)

# Simulation time tests
max_n = 10000
numPoints = 10
lag = max_n//numPoints
with open('tests/logs/data.log', 'w') as f:
	for n in range(0, max_n+1, lag):
		start = time()
		env = simpy.Environment()
		params['numMiners'] = n
		simulate(env, params)
		env.run(until = params['simulationTime'])
		
		stop = time()
		f.write("%d %5.5f\n"%(n, stop-start))
