def broadcast(env, object, objectType, source, neighbourList, params, pipes="", allNodes=""):
	"""Broadcasts the object from the source to destination"""
	if objectType == "Transaction":
		"""Broadcast a transaction to all neighbours"""
		for neighbour in neighbourList:
			sourceLocation = "Ireland"
			env.process(allNodes[neighbour].transactionPool.putTransaction(object, sourceLocation))

	elif objectType == "Block":
		"""Broadcast a block to all neighbours"""
		if not pipes:
			raise RuntimeError('There are no output pipes.')
		events = []
		for neighbour in neighbourList:
			# Obtain transmission delay
			sourceLocation = allNodes[neighbour].location
			store = pipes[neighbour]
			events.append(store.put(object, sourceLocation))

		if bool(params['verbose']):
			print("%7.4f" % env.now+" : "+"Node %s propagated Block %s" %
					(source, object.identifier))
		return env.all_of(events)
