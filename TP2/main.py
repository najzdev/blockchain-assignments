# from cryptography.hazmat.primitives.asymmetric import rsa, padding
# from cryptography.hazmat.primitives import serialization, hashes
# # Génération d’une paire de clés RSA 2048 bits
# private_key = rsa.generate_private_key(
#  public_exponent=65537,
#  key_size=4096
# )
# public_key = private_key.public_key()
# print("Clés RSA générées avec succès")

# =====

import time
from cryptography.hazmat.primitives.asymmetric import rsa

# Test avec 2048 ou 4096 bits
KEY_SIZE = 2048  # Changez à 2048 pour comparer

start_time = time.perf_counter()

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=KEY_SIZE
)
public_key = private_key.public_key()

end_time = time.perf_counter()
execution_time = end_time - start_time

print(f"Clés RSA de {KEY_SIZE} bits générées en : {execution_time:.4f} secondes")

# 1. Why a longer key is safer, but slower?
# Safer: Doubling the key size exponentially increases the mathematical difficulty of factoring large prime numbers, making attacks vastly harder.

# Slower: It requires intensive math to generate and consumes more CPU cycles to process larger numbers during encryption, decryption, and verification.