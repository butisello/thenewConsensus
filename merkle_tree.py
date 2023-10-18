from Crypto.Hash import SHA256

class MerkleTree:

    def __init__(self, transactions):
        self.transactions = transactions
        self.tree = []
        self.create_tree()

    def create_tree(self):
        transaction_hashes = [SHA256.new(str(tx).encode('utf-8')).digest() for tx in self.transactions]
        self.tree.append(transaction_hashes)
        while len(transaction_hashes) > 1:
            transaction_hashes = self.combine_hashes(transaction_hashes)
            self.tree.append(transaction_hashes)

    def combine_hashes(self, hashes):
        combined = []
        for i in range(0, len(hashes), 2):
            if i+1 < len(hashes):
                combined_hash = SHA256.new(hashes[i] + hashes[i+1]).digest()
            else:
                combined_hash = SHA256.new(hashes[i]).digest()
            combined.append(combined_hash)
        return combined

    def get_root(self):
        return self.tree[-1][0]
