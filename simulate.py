import simpy
from block import Block
from network import Network

def blockGenerator(name, miner, params):
	"""Block generator"""
	b = Block(name, params)
	return b

def transactionGenerator(id, params):
	"""Transaction generator"""
	t = Transaction(id, params)
	return t

def simulate(miner, params):
	"""Begin simulation"""
	blist = []
	n = Network("Net1")
	for i in range(1, 6):
		delay = i
		b = blockGenerator("Block%d"%i, miner, params)
		blist.append(b)
		b.validate(env, miner, delay)
		print(b.name+" started validation at %7.4f"%env.now)
		yield env.timeout(delay)
		print(b.name+" validated at %7.4f"%env.now)
		n.addBlock(b)
		n.propagate()


env = simpy.Environment()
minerCapacity = 2
miner = simpy.Resource(env, capacity = minerCapacity)
params = 10
env.process(simulate(miner, params))
env.run(until = 30)