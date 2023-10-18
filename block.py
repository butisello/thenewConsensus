import time

class Block:
    def __init__(self, blockCount, transactions, lastHash=''):
        self.blockCount = blockCount
        self.transactions = transactions
        self.lastHash = lastHash
        self.timestamp = time.time()
        self.signature = ''

    @staticmethod
    def genesis():
        return Block(0, [], 'genesis_hash')
