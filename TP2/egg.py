from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# 1. Generate the RSA key pair first (from Exercise 1.1)
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()
print("Clés RSA générées avec succès")

# 2. Encrypt and decrypt message (from Exercise 1.2)[cite: 1]
message = b"Blockchain et cryptographie asymetrique"

# Chiffrement
ciphertext = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Déchiffrement
plaintext = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("Message initial :", message)
print("Message déchiffré :", plaintext.decode())





# Encryption uses the public exponent $e$:$$c = m^e \pmod n$$

# Decryption uses the private exponent $d$:$$m = c^d \pmod n$$

# 2. Why can't you use the public key to decrypt?
# The public key only holds the components needed to encrypt data. The secret numbers and parameters required to reverse the math and decrypt it are stored exclusively inside the private key.
