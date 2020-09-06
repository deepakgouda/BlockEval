# Design and Validation of BlockEval, a Blockchain Simulator

In this repository, we introduce the design and architecture of our
blockchain simulator, BlockEval, which mimics the behaviour
of concurrent operations that occur in a real-life blockchain
system.

BlockEval can be extended to simulate any blockchain framework. In 
the provided implementation, we show the Proof-of-Work implementation
of BlockEval.

We use Python (3.7+) and Simpy, a popular process-based
discrete-event simulation framework developed in standard
Python to implement the simulator.

## Installation Instructions
* Clone the github repo
``` 
git clone https://github.com/deepakgouda/BlockEval.git 
```
* Install Python 3.7+
* Install the necessary packages using `cd BlockEval && pip install -r requirements.txt`

## Setup Instructions
* Create directories `params`, `dumps` and `output` in the current directory.
``` 
mkdir params dumps output
```
* Define the necessary parameters in `params.json` and move it into `params` folder.
``` 
mv params.json params/
```
* Run the simulator using
``` 
python simulate.py params/params.json dumps/netDump.pkl > output/output.log 
```
* Find the output logs in `output/output.log`. 
* Further statistics can be drawn from the pickle dump file `dumps/netDump.pkl`. It is a python dict containing the neighbour list, location, blockchain, data statistics of each node in the network.
``` 
>>> with open("dumps/netDump.pkl", "rb") as f:
        netDump = pickle.load(f)
```
