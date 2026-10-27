# Initial signed message
message = b"Transaction : Alice -> Bob : 3 BTC"

# Modifying the message after signing
modified_message = b"Transaction : Alice -> Bob : 100 BTC"

try:
    public_key.verify(
        signature,
        modified_message,  # Using the modified message
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print("Valid signature - the message is authentic.")
except Exception:
    print("Invalid signature.")


    #Why?
# Hashing Effect: The signature is calculated using the cryptographic fingerprint (SHA-256 hash) of the initial message. The slightest change to a character or byte in the message produces a completely different hash.
# 
# Integrity and Authentication Guarantee: Because the new hash no longer matches the one originally signed with the private key, the verification function using the public key fails. This proves that any attempt to tamper with or alter the message in transit is immediately detected.