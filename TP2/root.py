import time
import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

# --- Helper functions from previous exercises ---
def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def hash_pair(left: str, right: str) -> str:
    return sha256_hex(bytes.fromhex(left) + bytes.fromhex(right))

def make_leaf_hashes(transactions):
    return [sha256_hex(tx.encode()) for tx in transactions]

def merkle_root(leaf_hashes):
    if not leaf_hashes:
        return ''
    current = leaf_hashes
    while len(current) > 1:
        if len(current) % 2 == 1:
            current.append(current[-1])
        current = [hash_pair(current[i], current[i+1]) for i in range(0, len(current), 2)]
    return current[0]

def signer_message(privkey, msg: bytes) -> bytes:
    return privkey.sign(
        msg,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )

def verifier_signature(pubkey, msg: bytes, sig: bytes) -> bool:
    try:
        pubkey.verify(
            sig,
            msg,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        return True
    except:
        return False

# --- Block Class Definition ---
class Block:
    def __init__(self, index, transactions, prev_hash, miner_private_key):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.prev_hash = prev_hash
        self.merkle_root = merkle_root(make_leaf_hashes(transactions))
        
        # Global block hash
        header = f"{self.index}{self.timestamp}{self.merkle_root}{self.prev_hash}".encode()
        self.hash = sha256_hex(header)
        
        # Miner signature
        self.signature = signer_message(miner_private_key, self.hash.encode())

    def verify_block(self, miner_public_key):
        """Vérifie la signature et la validité interne du bloc."""
        header = f"{self.index}{self.timestamp}{self.merkle_root}{self.prev_hash}".encode()
        return verifier_signature(miner_public_key, sha256_hex(header).encode(), self.signature)

# --- RSA Key Generation for Testing ---
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

# --- Simulation ---
block = Block(1, ["Alice->Bob:2", "Bob->Charlie:1"], "000000abc", private_key)
print("Hash du bloc :", block.hash)
print("Merkle Root :", block.merkle_root)
print("Signature valide :", block.verify_block(public_key))