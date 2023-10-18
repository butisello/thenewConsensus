from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from merkle_tree import MerkleTree


class TransactionPool:
    def __init__(self, consensus_algorithm):
        self.transactions = []
        self.max_transactions = 5
        self.consensus = consensus_algorithm

    def add_transaction(self, transaction):        
        # Verify the transaction's signature
        sender_public_key = RSA.import_key(transaction.senderPublicKey)
        if transaction.verify_signature(sender_public_key):
            if not self.transaction_exists(transaction.id):
                self.transactions.append(transaction)
                if self.is_full():
                    # Create a shallow copy of the transactions
                    temp_transactions = self.transactions.copy()
                    
                    # Generate the Merkle root from the temporary list
                    merkle_tree = MerkleTree(temp_transactions)
                    merkle_root = merkle_tree.get_root()
                    
                    # Clear the main transaction pool
                    self.transactions = []
                    
                    # Trigger the handle_full_transaction_pool method in ErdosConsensus
                    self.consensus.handle_full_transaction_pool(merkle_root, temp_transactions)



    def remove_transaction(self, transaction_id):
        self.transactions = [tx for tx in self.transactions if tx.id != transaction_id]

    def transaction_exists(self, transaction_id):
        return any(tx.id == transaction_id for tx in self.transactions)

    def is_full(self):
        return len(self.transactions) >= self.max_transactions
