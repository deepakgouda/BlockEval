from utils import getTransmissionDelay

def broadcast(env, object, objectType, source, neighbourList, params, pipes="", miners=""):
	"""Broadcasts the object from the source to destination"""
	if objectType == "Transaction":
		"""Broadcast a transaction to all neighbours"""
		for neighbour in neighbourList:
			sourceLocation = "Ireland"
			destLocation = miners[neighbour].location
			delay = getTransmissionDelay(sourceLocation, destLocation)
			env.process(miners[neighbour].transactionPool.putTransaction(object, delay))

	elif objectType == "Block":
		"""Broadcast a block to all neighbours"""
		if not pipes:
			raise RuntimeError('There are no output pipes.')
		events = []
		for neighbour in neighbourList:
			# Obtain transmission delay
			sourceLocation = miners[neighbour].location
			destLocation = miners[neighbour].location
			delay = getTransmissionDelay(sourceLocation, destLocation)

			store = pipes[neighbour]
			events.append(store.put(object, delay))

		if bool(params['verbose']):
			print("%7.4f" % env.now+" : "+"Miner %s propagated Block %s" %
					(source, object.identifier))
		return env.all_of(events)

	elif objectType == "Interrupt":
		"""Broadcast an interrupt to all neighbours"""
		if not pipes:
			raise RuntimeError('There are no output pipes.')
		events = []
		for neighbour in neighbourList:
			# Obtain transmission delay
			sourceLocation = miners[neighbour].location
			destLocation = miners[neighbour].location
			delay = getTransmissionDelay(sourceLocation, destLocation)

			store = pipes[neighbour]
			store.sendInterrupt(miners[neighbour], delay)
		return env.all_of(events)
