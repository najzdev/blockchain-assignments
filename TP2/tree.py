import hashlib

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

def merkle_proof(leaf_hashes, index):
    proof = []
    idx = index
    current = leaf_hashes.copy()
    while len(current) > 1:
        if len(current) % 2 == 1:
            current.append(current[-1])
        sibling_idx = idx ^ 1
        sibling_hash = current[sibling_idx]
        is_left = sibling_idx < idx
        proof.append((sibling_hash, is_left))
        idx //= 2
        current = [hash_pair(current[i], current[i+1]) for i in range(0, len(current), 2)]
    return proof

def verify_proof(leaf_hash, proof, root):
    computed = leaf_hash
    for sibling, is_left in proof:
        if is_left:
            computed = hash_pair(sibling, computed)
        else:
            computed = hash_pair(computed, sibling)
    return computed == root

# 1. Transactions and initial Merkle tree setup[cite: 4]
txs = ["Alice->Bob:5", "Bob->Charlie:3", "Dave->Eve:1"]
leaf_hashes = make_leaf_hashes(txs)
root = merkle_root(leaf_hashes)
print("Merkle Root:", root)

# 2. Proof test for index 1
idx = 1
proof = merkle_proof(leaf_hashes, idx)
print("Transaction:", txs[idx])
print("Proof valide:", verify_proof(leaf_hashes[idx], proof, root))

# 3. TAF: Modify a transaction and verify again[cite: 5]
txs_modifiees = txs.copy()
txs_modifiees[idx] = "Bob->Charlie:999"  # Modified transaction

leaf_hashes_modifies = make_leaf_hashes(txs_modifiees)
root_modifiee = merkle_root(leaf_hashes_modifies)

print("Test avec la nouvelle racine :", verify_proof(leaf_hashes[idx], proof, root_modifiee))