def poli_encrypt(text, key=""):
    plain_alphabet = "AĄBCĆDEĘFGHIJKLŁMNŃOÓPRSŚTUVWXYZŹŻ"
    qwerty_alphabet = "QWERTYUIOPASDFGHJKLZXCVBNMĄĆĘŁŃÓŚŹŻ"

    if key == "":
        key = qwerty_alphabet
    
    key = key.upper()
    
    result = ""
    key_index = 0
    key_length = len(key)
    
    for char in text:
        if char.isalpha():
            text_index = plain_alphabet.index(char.upper())
            key_char = key[key_index % key_length]
            key_index_shift = plain_alphabet.index(key_char)

            encrypted_index = (text_index + key_index_shift) % len(plain_alphabet)
            encrypted_char = plain_alphabet[encrypted_index]

            result += encrypted_char if char.isupper() else encrypted_char.lower()
            
            key_index += 1
        else:
            result += char
    
    return result

def poli_decrypt(encrypted_text, key=""):
    plain_alphabet = "AĄBCĆDEĘFGHIJKLŁMNŃOÓPRSŚTUVWXYZŹŻ"
    qwerty_alphabet = "QWERTYUIOPASDFGHJKLZXCVBNMĄĆĘŁŃÓŚŹŻ"

    if key == "":
        key = qwerty_alphabet
    
    key = key.upper()
    
    result = ""
    key_index = 0
    key_length = len(key)
    
    for char in encrypted_text:
        if char.isalpha():
            text_index = plain_alphabet.index(char.upper())
            key_char = key[key_index % key_length]
            key_index_shift = plain_alphabet.index(key_char)

            decrypted_index = (text_index - key_index_shift) % len(plain_alphabet)
            decrypted_char = plain_alphabet[decrypted_index]

            result += decrypted_char if char.isupper() else decrypted_char.lower()
            
            key_index += 1
        else:
            result += char  
    
    return result
