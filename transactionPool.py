from transaction import Transaction
from broadcast import broadcast
import numpy as np

class TransactionPool:
    """Transaction pool for a miner"""
    def __init__(self, env, identifier, neighbourList, miners, params):
        self.env = env
        self.identifier = identifier
        self.neighbourList = neighbourList
        self.params = params
        self.miners = miners
        self.transactionList = []
    
    def getTransaction(self, transactionCount):
        transactionCount = min(transactionCount, len(self.transactionList))
        transactions = self.transactionList[:transactionCount]
        return transactions

    def popTransaction(self, transactionCount):
        transactionCount = min(transactionCount, len(self.transactionList))
        self.transactionList = self.transactionList[transactionCount:]

    def putTransaction(self, transaction, source):
        delay = 0.5
        yield self.env.timeout(delay)
        if transaction not in self.transactionList:
            self.transactionList.append(transaction)
            print("%7.4f : %s accepted by %s"%(self.env.now, transaction.identifier, self.identifier))
            broadcast(self.env, transaction, "Transaction", self.identifier, \
                            self.neighbourList, self.params, miners=self.miners)
        


