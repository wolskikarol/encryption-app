def mono_encrypt(text, key=""):
    plain_alphabet = "AĄBCĆDEĘFGHIJKLŁMNŃOÓPRSŚTUVWXYZŹŻ"

    if key == "":
        qwerty_alphabet = "QWERTYUIOPASDFGHJKLZXCVBNMĄĆĘŁŃÓŚŹŻ"
    else:
        key = key.upper()
        key = ''.join(sorted(set(key), key=key.index))
        qwerty_alphabet = key + ''.join([char for char in plain_alphabet if char not in key])

    encryption_map = {plain_alphabet[i]: qwerty_alphabet[i] for i in range(len(plain_alphabet))}
    encryption_map.update({plain_alphabet[i].lower(): qwerty_alphabet[i].lower() for i in range(len(plain_alphabet))})

    result = ""
    for char in text:
        if char in encryption_map:
            result += encryption_map[char]
        else:
            result += char
    
    return result

def mono_decrypt(encrypted_text, key=""):
    plain_alphabet = "AĄBCĆDEĘFGHIJKLŁMNŃOÓPRSŚTUVWXYZŹŻ"

    if key == "":
        qwerty_alphabet = "QWERTYUIOPASDFGHJKLZXCVBNMĄĆĘŁŃÓŚŹŻ"
    else:
        key = key.upper()
        key = ''.join(sorted(set(key), key=key.index))
        qwerty_alphabet = key + ''.join([char for char in plain_alphabet if char not in key])

    decryption_map = {qwerty_alphabet[i]: plain_alphabet[i] for i in range(len(plain_alphabet))}
    decryption_map.update({qwerty_alphabet[i].lower(): plain_alphabet[i].lower() for i in range(len(plain_alphabet))})

    result = ""
    for char in encrypted_text:
        if char in decryption_map:
            result += decryption_map[char]
        else:
            result += char
    
    return result
