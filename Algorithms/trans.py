def trans_encrypt(text, rows, columns, order):

    text = text.replace(" ", "_").upper()

    if len(text) % (rows * columns) != 0:
        text += 'X' * ((rows * columns) - len(text))

    matrix = []
    index = 0
    for i in range(rows):
        row = []
        for j in range(columns):
            if index < len(text):
                row.append(text[index])
                index += 1
            else:
                row.append('X')
        matrix.append(row)

    result = ''
    for column in order:
        for row in matrix:
            result += row[column - 1]

    return result


def trans_decrypt(encrypted_text, rows, columns, order):
    expected_length = rows * columns
    if len(encrypted_text) != expected_length:
        return f"Długość zaszyfrowanego tekstu ({len(encrypted_text)}) nie odpowiada rozmiarowi macierzy ({expected_length})."

    matrix = [[''] * columns for _ in range(rows)]

    indeks = 0
    for kolumna in order:
        for i in range(rows):
            matrix[i][kolumna - 1] = encrypted_text[indeks]
            indeks += 1

    decrypted_text = ''
    for row in matrix:
        decrypted_text += ''.join(row)

    decrypted_text = decrypted_text.rstrip('X')

    decrypted_text = decrypted_text.replace("_", " ")

    return decrypted_text
