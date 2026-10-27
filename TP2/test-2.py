from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

# 1. Generate the RSA key pair first
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()

# 2. Reusable functions
def signer_message(privkey, msg: bytes) -> bytes:
    """Retourne la signature RSA du message donné."""
    return privkey.sign(
        msg,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

def verifier_signature(pubkey, msg: bytes, sig: bytes) -> bool:
    """Retourne True si la signature est valide, False sinon."""
    try:
        pubkey.verify(
            sig,
            msg,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except:
        return False

# 3. Test
msg = b"Test de signature"
sig = signer_message(private_key, msg)
print("Valide ?", verifier_signature(public_key, msg, sig))