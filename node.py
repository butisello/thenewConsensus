from transaction import Transaction
from transaction_pool import TransactionPool
from block import Block
from wallet import Wallet
from erdos_consensus import ErdosConsensus

class Node:
    def __init__(self, consensus_algorithm):
        print("Creating a new Node...")
        self.chain = [Block.genesis()]
        self.consensus = consensus_algorithm
        self.transaction_pool = TransactionPool(self.consensus)
        self.wallet = Wallet()
        
        self.consensus.add_node(self)

    def add_block(self, block):
        if self.consensus.validate_block(block, self.chain):
            self.chain.append(block)
        else:
            print("Block validation failed!")

    def create_transaction(self, receiverPublicKey, amount, type):
        message = self.wallet.get_public_key().decode() + receiverPublicKey.decode() + str(amount) + type
        signature = self.wallet.sign(message)
        transaction = Transaction(self.wallet.get_public_key(), receiverPublicKey, amount, type, signature)
        if self.consensus.validate_transaction(transaction):
            self.transaction_pool.add_transaction(transaction)
            self.consensus.broadcast_transaction(transaction)
            return transaction
        else:
            print("Transaction validation failed!")
            return None

    def receive_transaction(self, transaction):
        if self.consensus.validate_transaction(transaction):
            self.transaction_pool.add_transaction(transaction)
        else:
            print("Received transaction is invalid!")

    def createProspectiveBlock(self, transactions):
        # Create a new block using the provided transactions
        new_block = Block(len(self.chain), transactions)
        
        # Further validation or processing can be done here if needed
        
        # For now, just print a message indicating the creation of a prospective block
        print("Prospective block created with", len(transactions), "transactions.")
        
        return new_block
