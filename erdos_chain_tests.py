import unittest
from erdos_consensus import ErdosConsensus
from node import Node
from transaction import Transaction
from block import Block
from wallet import Wallet
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256


class ErdosChainTests(unittest.TestCase):

    def setUp(self):
        self.consensus = ErdosConsensus()
        self.node1 = Node(self.consensus)
        self.node2 = Node(self.consensus)

    def test_transaction_creation_and_validation(self):
        tx = self.node1.create_transaction(self.node2.wallet.get_public_key(), 10, 'send')
        print("\nTransaction Created:")
        print(f"Sender: {tx.senderPublicKey}")
        print(f"Receiver: {tx.receiverPublicKey}")
        print(f"Amount: {tx.amount}")
        print(f"Type: {tx.type}")
        print(f"ID: {tx.id}")
        print(f"Timestamp: {tx.timestamp}")
        print(f"Fee: {tx.fee}")
        print(f"Signature: {tx.signature}")
        self.assertIsNotNone(tx, "Transaction creation failed!")
        self.assertTrue(self.consensus.validate_transaction(tx), "Transaction validation failed!")


    def test_add_and_remove_nodes(self):
        node3 = Node(self.consensus)
        print("\nNode Added to Network:")
        print(f"Node's Wallet Public Key: {node3.wallet.get_public_key().decode('utf-8')}")
        self.assertIn(node3, self.consensus.nodes, "Node not added to consensus!")
        self.consensus.remove_node(node3)
        self.assertNotIn(node3, self.consensus.nodes, "Node not removed from consensus!")


    def test_broadcast_transaction(self):
        tx = self.node1.create_transaction(self.node2.wallet.get_public_key(), 10, 'send')
        self.assertIn(tx, self.node2.transaction_pool.transactions, "Transaction not broadcasted to node2!")

    def test_block_validation_and_addition(self):
        # Create some transactions to fill the pool
        for _ in range(5):
            self.node1.create_transaction(self.node2.wallet.get_public_key(), 10, 'send')
        
        # Create a new block with transactions from node1's pool
        new_block = Block(len(self.node1.chain), self.node1.transaction_pool.transactions)
        
        # Add the block to node2's chain
        self.node2.add_block(new_block)
        
        self.assertIn(new_block, self.node2.chain, "Block not added to node2's chain!")
        self.assertTrue(self.consensus.validate_block(new_block, self.node2.chain), "Block validation failed!")

    def test_hashedDigits(self):
        # Create a transaction to get a timestamp
        tx = self.node1.create_transaction(self.node2.wallet.get_public_key(), 10, 'send')
        timestamp = tx.timestamp

        # Call the hashedDigits method
        hDigits = self.consensus.hashedDigits(timestamp)
        #print(f"AND THE SUBSET IS: {subset}")

        # Check the result
        self.assertIsNotNone(hDigits, "hashedDigits returned None for hDigits!")
        self.assertEqual(len(hDigits), 64, "hashedDigits did not return a 64-character hash for hDigits!")

        #self.assertIsNotNone(subset, "hashedDigits returned None for subset!")
        #self.assertEqual(len(subset), 7, "Subset is not 7 characters long!")

    def test_nearestNode(self):
        # Create 10 nodes and add them to the consensus
        #nodes = [Node(self.consensus) for _ in range(10)]
        nodes = []
        for _ in range(10):
            node = Node(self.consensus)
            nodes.append(node)
            print(node.wallet.get_public_key().decode('utf-8'))

        #for node in nodes:
            #theNode = Node()
            #self.consensus.add_node(node)
            #nodeKey = self.wallet.get_public_key()
            #print("\nI have been added: ", nodeKey.decode('utf-8'))
            #print(node.wallet.get_public_key().decode('utf-8'))

        #print("\nAdded Nodes:")
        #for node in nodes:
        #    print(node.wallet.get_public_key().decode('utf-8'))

        # Create a transaction to get a timestamp for hDigits generation
        tx = self.node1.create_transaction(self.node2.wallet.get_public_key(), 10, 'send')
        timestamp = tx.timestamp
        hDigits = self.consensus.hashedDigits(timestamp)

        # Call the nearestNode method
        nearest_node_key = self.consensus.nearestNode(hDigits)

        # Check the result
        self.assertIsNotNone(nearest_node_key, "nearestNode returned None!")
        print("\nhDigits:", hDigits)
        print("Nearest Node's Public Key:", nearest_node_key.decode('utf-8'))

    def test_verify_signature(self):
        # Create a transaction
        tx = self.node1.create_transaction(self.node2.wallet.get_public_key(), 10, 'send')

        # Verify the signature using the sender's public key
        sender_public_key = RSA.import_key(tx.senderPublicKey)
        self.assertTrue(tx.verify_signature(sender_public_key), "Transaction signature verification failed!")

        # Try verifying with a different public key (should fail)
        wrong_public_key = Wallet().get_public_key()
        self.assertFalse(tx.verify_signature(RSA.import_key(wrong_public_key)), "Transaction signature verification should have failed with wrong public key!")

    def test_add_transaction(self):
        # Create a transaction and add it to the pool
        tx1 = self.node1.create_transaction(self.node2.wallet.get_public_key(), 10, 'send')
        self.node1.transaction_pool.add_transaction(tx1)
        self.assertIn(tx1, self.node1.transaction_pool.transactions, "Transaction not added to the pool!")

        # Try adding the same transaction again (shouldn't be added)
        self.node1.transaction_pool.add_transaction(tx1)
        self.assertEqual(self.node1.transaction_pool.transactions.count(tx1), 1, "Duplicate transaction added to the pool!")

        # Fill the pool
        for _ in range(4):
            tx = self.node1.create_transaction(self.node2.wallet.get_public_key(), 10, 'send')
            self.node1.transaction_pool.add_transaction(tx)

        # Try adding another transaction when the pool is full (shouldn't be added)
        tx_overflow = self.node1.create_transaction(self.node2.wallet.get_public_key(), 10, 'send')
        self.node1.transaction_pool.add_transaction(tx_overflow)
        self.assertNotIn(tx_overflow, self.node1.transaction_pool.transactions, "Transaction added even though the pool was full!")




if __name__ == '__main__':
    unittest.main()
