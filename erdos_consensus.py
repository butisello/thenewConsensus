import random
from Crypto.Hash import SHA256

class ErdosConsensus:
    def __init__(self):
        self.nodes = []
        self.excluded_public_keys = set()  # Use a set to ensure uniqueness

    def add_node(self, node):
        """Add a new node to the network."""
        if node not in self.nodes:
            self.nodes.append(node)


    def remove_node(self, node):
        """Remove a node from the network."""
        self.nodes.remove(node)

    def broadcast_transaction(self, transaction):
        """Broadcast a transaction to all nodes in the network."""
        for node in self.nodes:
            node.receive_transaction(transaction)

    def broadcast_block(self, block):
        """Broadcast a new block to all nodes in the network."""
        for node in self.nodes:
            node.add_block(block)

    def validate_transaction(self, transaction):
        # Implement validation logic for a transaction
        # For now, we'll just return True
        return True

    def validate_block(self, block, blockchain):
        # Implement validation logic for a block against the given blockchain
        # For now, we'll just return True
        return True

    def hashedDigits(self, timestamp):
        # Convert the timestamp to string and hash it
        hashedTime = SHA256.new(str(timestamp).encode('utf-8')).hexdigest()

        # Generate a random integer between 1 and 64
        randInt = random.randint(1, 64)

        # Ensure the extraction does not exceed the length of hashedTime
        start_index = randInt
        end_index = start_index + 7
        if end_index > len(hashedTime):
            start_index = len(hashedTime) - 7
            end_index = len(hashedTime)

        # Extract the 7-character subset
        subset = hashedTime[start_index:end_index]

        # Hash the subset
        hDigits = SHA256.new(subset.encode('utf-8')).hexdigest()

        return hDigits

    def nearestNode(self, hDigits):
        nearest_node_key = None
        nearest_distance = float('inf')  # Initialize with infinity

        for node in self.nodes:
            node_key = node.wallet.get_public_key()
            hashed_node_key = SHA256.new(node_key).hexdigest()

            # Compute the difference between the two hashes
            distance = abs(int(hashed_node_key, 16) - int(hDigits, 16))

            # Update if this node's key is nearer to hDigits
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_node_key = node_key

        return nearest_node_key

    def selectForger(self, hDigits, excluded_public_keys=[]):
        forger = None
        nearest_distance = float('inf')  # Initialize with infinity

        for node in self.nodes:
            node_key = node.wallet.get_public_key()
            
            # Skip nodes that are in the excluded list
            if node_key in excluded_public_keys:
                continue

            hashed_node_key = SHA256.new(node_key).hexdigest()

            # Compute the difference between the two hashes
            distance = abs(int(hashed_node_key, 16) - int(hDigits, 16))

            # Update if this node's key is nearer to hDigits
            if distance < nearest_distance:
                nearest_distance = distance
                forger = node_key

        return forger


    def handle_full_transaction_pool(self, temp_transactions):
        excluded_public_keys = [tx.senderPublicKey for tx in temp_transactions] + [tx.receiverPublicKey for tx in temp_transactions]
        hDigits = self.hashedDigits(temp_transactions[-1].timestamp)
        forger = self.selectForger(hDigits, excluded_public_keys)
        # Find the forger node based on the public key
        forger_node = next(node for node in self.nodes if node.wallet.get_public_key() == forger)

        # Send a message to the forger to create a prospective block
        prospective_block = forger_node.createProspectiveBlock(temp_transactions)

        # Further processing or validation can be done here if needed
        
        # For now, just print a message indicating the forger
        print("Forger selected:", forger.decode('utf-8'))
        

    

    # Add other methods or logic specific to the ErdosConsensus algorithm


