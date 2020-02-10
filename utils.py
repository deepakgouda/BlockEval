import numpy as np
import json

def getBlockDelay(mu, sigma):
    return mu + sigma*np.random.randn()


def getTransmissionDelay(source, destination):
    with open('params.json', 'r') as f:
	    params = f.read()
    params = json.loads(params)
    mu = params["delay"][source][destination]["mu"]
    sigma = params["delay"][source][destination]["sigma"]
    return mu + sigma*np.random.randn()
