def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for char in plaintext:
        if char.isalpha() != 0:
            char_index = ord(char)
            if 97 <= char_index <= 122:
                char_index = char_index + shift
                if char_index > 122:
                    char_index = char_index - 26
                ciphered_char = chr(char_index)
                ciphertext += ciphered_char
            elif 65 <= char_index <= 90:
                char_index = char_index + shift
                if char_index > 90:
                    char_index = char_index - 26
                ciphered_char = chr(char_index)
                ciphertext += ciphered_char
        else:
            ciphertext += char
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for char in ciphertext:
        if char.isalpha() != 0:
            char_index = ord(char)
            if 97 <= char_index <= 122:
                char_index = char_index - shift
                if char_index < 97:
                    char_index = char_index + 26
                plain_char = chr(char_index)
                plaintext += plain_char
            elif 65 <= char_index <= 90:
                char_index = char_index - shift
                if char_index < 65:
                    char_index = char_index + 26
                plain_char = chr(char_index)
                plaintext += plain_char
        else:
            plaintext += char
    return plaintext
