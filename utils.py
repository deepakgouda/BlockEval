import numpy as np
import json

def getBlockDelay(mu, sigma):
    delay = mu + sigma*np.random.randn()
    if delay < 0:
        return getBlockDelay(mu, sigma)
    return delay

def getTransactionDelay(mu, sigma):
    delay = mu + sigma*np.random.randn()
    if delay < 0:
        return getTransactionDelay(mu, sigma)
    return delay


def getTransmissionDelay(source, destination):
    with open('params.json', 'r') as f:
	    params = f.read()
    params = json.loads(params)
    mu = params["delay"][source][destination]["mu"]
    sigma = params["delay"][source][destination]["sigma"]
    delay = mu + sigma*np.random.randn()
    if delay < 0:
        return getTransmissionDelay(source, destination)
    return delay*600
