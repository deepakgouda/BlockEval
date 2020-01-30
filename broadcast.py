def broadcast(env, object, objectType, source, neighbourList, params, pipes="", miners=""):
	"""Broadcasts the object from the source to destination"""
	if objectType == "Transaction":
		"""Broadcast a transaction to all neighbours"""
		for neighbour in neighbourList:
			env.process(miners[neighbour].transactionPool.putTransaction(object, source))
	elif objectType == "Block":
		"""Broadcast a block to all neighbours"""
		if not pipes:
			raise RuntimeError('There are no output pipes.')
		events = []
		for neighbour in neighbourList:
			store = pipes[neighbour]
			events.append(store.put(object, source))

		if bool(params['verbose']):
			print("%7.4f" % env.now+" : "+"Miner %s propagated Block %s" %
					(source, object.identifier))
		return env.all_of(events)  # Condition event for all "events"
	elif objectType == "Interrupt":
		"""Broadcast an interrupt to all neighbours"""
		if not pipes:
			raise RuntimeError('There are no output pipes.')
		events = []
		for neighbour in neighbourList:
			store = pipes[neighbour]
			store.sendInterrupt(miners[neighbour], source)
		return env.all_of(events)  # Condition event for all "events"
