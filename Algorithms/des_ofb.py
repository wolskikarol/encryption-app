from Crypto.Cipher import DES

def des_ofb_encrypt(data, key, iv):    
    cipher = DES.new(key, DES.MODE_OFB, iv=iv)
    encrypted_data = cipher.encrypt(data)
    return encrypted_data

def des_ofb_decrypt(encrypted_data, key, iv):
    cipher = DES.new(key, DES.MODE_OFB, iv=iv)
    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data

