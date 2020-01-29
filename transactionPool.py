from transaction import Transaction
from broadcast import broadcast
import numpy as np

class TransactionPool:
    """Generate transactions in network"""
    def __init__(self, env, neighbourList, identifier, miners, params):
        self.env = env
        self.neighbourList = neighbourList
        self.identifier = identifier
        self.params = params
        self.miners = miners
        self.env.process(self.addTransaction())
        self.transactionList = []
    
    def addTransaction(self):
        num = 0
        while True:
            delay = (self.params['transactionMu']+self.params['transactionSigma']*np.random.randn(1))[0]
            yield self.env.timeout(delay)
            transaction = (Transaction("Transaction%d"%num, self.env.now))
            if bool(self.params['verbose']):
                print("%7.4f" % self.env.now+" : " +"%s added Transaction%d" % (self.identifier, num))
            # Broadcast transactions to all neighbours
            broadcast(self.env, transaction, "Transaction", self.identifier, \
                        self.neighbourList, self.params, miners=self.miners)
            num+=1
    
    def getTransaction(self, transactionCount):
        transactionCount = min(transactionCount, len(self.transactionList))
        transactions = self.transactionList[:transactionCount]
        self.transactionList = self.transactionList[transactionCount:]
        delay = 0.5
        self.env.timeout(delay)
        return transactions

    def putTransaction(self, transaction, source):
        delay = 0.5
        self.env.timeout(delay)
        if transaction not in self.transactionList:
            self.transactionList.append(transaction)
        else:
            print("%7.4f : %s rejected by %s"%(transaction.identifier, self.identifier))


