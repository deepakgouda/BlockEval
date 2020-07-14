import simpy
from utils import getTransmissionDelay

class Pipe(object):
    """This class represents the propagation through a cable."""

    def __init__(self, env, identifier, allNodes):
        self.env = env
        self.allNodes = allNodes
        self.identifier = identifier
        self.store = simpy.Store(self.env)

    def latencyPut(self, value, delay):
        yield self.env.timeout(delay)
        return self.store.put(value)

    def put(self, value, sourceLocation):
        # Simulate transmission delay
        # yield self.env.timeout(value.size * 1000)
        destLocation = self.allNodes[self.identifier].location
        delay = getTransmissionDelay(sourceLocation, destLocation)
        delay = delay + value.size * 10
        return self.env.process(self.latencyPut(value, delay))

    def get(self):
        return self.store.get()
