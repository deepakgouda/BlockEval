import simpy

class Pipe(object):
    """This class represents the propagation through a cable."""

    def __init__(self, env, identifier):
        self.env = env
        self.identifier = identifier
        self.store = simpy.Store(self.env)

    def latency(self, value, delay):
        yield self.env.timeout(delay)
        return self.store.put(value)

    def put(self, value, srcID):
        delay = 0.5
        return self.env.process(self.latency(value, delay))

    def get(self):
        return self.store.get()
