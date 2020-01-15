import simpy

class Block:
	"""docstring for Block"""
	def __init__(self, name, params):
		self.name=name
		self.params=params

	def validate(self, env, miner, delay):
		# while True:
		with miner.request() as request:
			print(request)
			yield request

			print('%s validated at %d ' % (self.name, env.now))
			yield env.timeout(delay)
			print('%s validated again at %d ' % (self.name, env.now))
