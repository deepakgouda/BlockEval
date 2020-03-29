import numpy as np
from broadcast import broadcast
from transaction import Transaction
from utils import getTransmissionDelay

class TransactionPool:
    """Transaction pool for a miner"""
    def __init__(self, env, identifier, neighbourList, allNodes, params):
        self.env = env
        self.identifier = identifier
        self.neighbourList = neighbourList
        self.params = params
        self.allNodes = allNodes
        self.transactionList = []
        self.prevTransactions = []
    
    def getTransaction(self, transactionCount):
        """Returns transactionCount number of Transactions. Ideally, should 
        return top transactions based on miner reward"""
        transactionCount = min(transactionCount, len(self.transactionList))
        transactions = self.transactionList[:transactionCount]
        return transactions

    def popTransaction(self, transactionCount):
        """Remove transactions from transaction pool. Called when transactions 
        are added by a received block or a block is mined."""
        transactionCount = min(transactionCount, len(self.transactionList))
        self.prevTransactions = self.transactionList[:transactionCount]
        self.transactionList = self.transactionList[transactionCount:]

    def putTransaction(self, transaction, sourceLocation):
        """Add received transaction to the transaction pool and broadcast further"""
        destLocation = self.allNodes[self.identifier].location
        delay = getTransmissionDelay(sourceLocation, destLocation)
        yield self.env.timeout(delay)
        if transaction not in self.transactionList and transaction not in self.prevTransactions:
            self.transactionList.append(transaction)
            broadcast(self.env, transaction, "Transaction", self.identifier, \
                        self.neighbourList, self.params, allNodes=self.allNodes)

            if bool(self.params['verbose']):
                print("%7.4f : %s accepted by %s"%(self.env.now, transaction.identifier, self.identifier))
        


