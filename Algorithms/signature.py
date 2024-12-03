from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    return private_key, public_key

def sign_message(private_key, message):
    message_bytes = message.encode('utf-8')
    signature = private_key.sign(
        message_bytes,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return signature

def verify_signature(public_key, message, signature):
    message_bytes = message.encode('utf-8')
    try:
        public_key.verify(
            signature,
            message_bytes,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        print("Podpis jest prawidłowy.")
    except InvalidSignature:
        print("Podpis jest nieprawidłowy.")

if __name__ == "__main__":
    private_key, public_key = generate_keys()

    message = "To jest wiadomość."

    signature = sign_message(private_key, message)
    print("Podpis:", signature)

    verify_signature(public_key, message, signature)
