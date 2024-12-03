from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os

def generate_rsa_keys(bits=2048):
    private_key = RSA.generate(bits)
    public_key = private_key.publickey()
    return public_key, private_key

def encrypt_data_rsa(input_data, public_key, is_file=False, output_file=None):
    if is_file:
        with open(input_data, 'rb') as file:
            data = file.read()
    else:
        data = input_data.encode('utf-8')
    
    max_chunk_size = public_key.size_in_bytes() - 42
    chunks = [data[i:i+max_chunk_size] for i in range(0, len(data), max_chunk_size)]
    
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_chunks = [cipher_rsa.encrypt(chunk) for chunk in chunks]
    
    if output_file and is_file:
        with open(output_file, 'wb') as file:
            for chunk in encrypted_chunks:
                file.write(chunk)
        return f"Zaszyfrowane dane zapisano w pliku: {output_file}"
    
    return encrypted_chunks

def decrypt_data_rsa(encrypted_chunks, private_key, is_file=False, output_file=None):
    cipher_rsa = PKCS1_OAEP.new(private_key)
    decrypted_data = b"".join(cipher_rsa.decrypt(chunk) for chunk in encrypted_chunks)
    
    if is_file and output_file:
        with open(output_file, 'wb') as file:
            file.write(decrypted_data)
        return f"Odszyfrowane dane zapisano w pliku: {output_file}"
    
    return decrypted_data.decode('utf-8')
