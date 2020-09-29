def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    for index, element in enumerate(plaintext):
        shift_alpha = keyword[index % len(keyword)]
        shift = ord((shift_alpha).lower()) - ord("a")
        if element.isalpha() != 0 and shift != 0:
            char_index = ord(element)
            if 97 <= char_index <= 122:
                char_index = char_index + shift
                if char_index > 122:
                    char_index = char_index - 26
                cipher_char = chr(char_index)
                ciphertext += cipher_char
            elif 65 <= char_index <= 90:
                char_index = char_index + shift
                if char_index > 90:
                    char_index = char_index - 26
                cipher_char = chr(char_index)
                ciphertext += cipher_char
        else:
            ciphertext += element
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    for index, element in enumerate(ciphertext):
        shift_alpha = keyword[index % len(keyword)]
        shift = ord((shift_alpha).lower()) - ord("a")
        if element.isalpha() != 0 and shift != 0:
            char_index = ord(element)
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
            plaintext += element
    return plaintext

# For commit
