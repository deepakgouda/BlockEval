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
# Simulation time tests : Varying Simulation Time
# max_n = 100000
# numPoints = 10
# lag = max_n//numPoints
# with open('tests/logs/simTime.log', 'w') as f:
# 	for n in range(10, max_n+1, lag):
# 		start = time()

# 		env = simpy.Environment()
# 		params['simulationTime'] = n
# 		simulate(env, params)
# 		env.run(until = params['simulationTime'])
		
# 		stop = time()
# 		f.write("%d %5.5f\n"%(n, stop-start))
