import simpy
from utils import getTransmissionDelay

class Pipe(object):
    """This class represents the propagation through a cable."""

    def __init__(self, env, identifier, miners):
        self.env = env
        self.miners = miners
        self.identifier = identifier
        self.store = simpy.Store(self.env)

    def latencyPut(self, value, delay):
        yield self.env.timeout(delay)
        return self.store.put(value)

    def put(self, value, sourceLocation):
        destLocation = self.miners[self.identifier].location
        delay = getTransmissionDelay(sourceLocation, destLocation)
        return self.env.process(self.latencyPut(value, delay))

    def latencyInterrupt(self, delay, miner):
        yield self.env.timeout(delay)
        miner.blockGeneratorAction.interrupt()

    def sendInterrupt(self, miner, sourceLocation):
        destLocation = self.miners[self.identifier].location
        delay = getTransmissionDelay(sourceLocation, destLocation)
        self.env.process(self.latencyInterrupt(delay, miner))

    def get(self):
        return self.store.get()
