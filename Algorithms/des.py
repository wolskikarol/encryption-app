from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

def des_encrypt(data, key):
    des = DES.new(key, DES.MODE_ECB)
    padded_data = pad(data, DES.block_size)
    encrypted_data = des.encrypt(padded_data)
    return encrypted_data

def des_decrypt(encrypted_data, key):
    des = DES.new(key, DES.MODE_ECB)
    decrypted_data = des.decrypt(encrypted_data)
    unpadded_data = unpad(decrypted_data, DES.block_size)
    return unpadded_data

