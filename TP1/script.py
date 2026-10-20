import hashlib
import json

class Block:
    def __init__(self, index, timestamp, data, previous_hash=''):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.create_hash()

    def create_hash(self):
        # Concatenate block attributes into a single string
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}".encode()
        # Return the SHA-256 hexadecimal digest
        return hashlib.sha256(block_string).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }

# Initialize the blockchain list
blockchain = []

# 1. Create the Genesis Block (index 0)
genesis_block = Block(0, "2025-10-12 00:00", "Bloc de genèse", previous_hash="0")
blockchain.append(genesis_block)

# 2. Create Block 1, linked to the Genesis block's hash
block1 = Block(1, "2025-10-12 00:05", "Alice envoie 5 BTC", previous_hash=blockchain[-1].hash)
blockchain.append(block1)

# 3. Create Block 2, linked to Block 1's hash
block2 = Block(2, "2025-10-12 00:10", "Bob envoie 3 BTC", previous_hash=blockchain[-1].hash)
blockchain.append(block2)

# Print the final blockchain as a clean JSON structure
print(json.dumps([b.to_dict() for b in blockchain], indent=4))