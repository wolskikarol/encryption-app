from Crypto.Cipher import AES

def aes_ctr_encrypt( data, key, nonce):
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    encrypted_data = cipher.encrypt(data)
    return encrypted_data

def aes_ctr_decrypt(encrypted_data, key, nonce):
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data

