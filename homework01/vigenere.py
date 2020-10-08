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
        if element.isalpha() and shift != 0:
            char_index = ord(element)
            if ord("a") <= char_index <= ord("z"):
                char_index = char_index + shift
                if char_index > ord("z"):
                    char_index = char_index - 26
                cipher_char = chr(char_index)
                ciphertext += cipher_char
            elif ord("A") <= char_index <= ord("Z"):
                char_index = char_index + shift
                if char_index > ord("Z"):
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
        if element.isalpha() and shift != 0:
            char_index = ord(element)
            if ord("a") <= char_index <= ord("z"):
                char_index = char_index - shift
                if char_index < ord("a"):
                    char_index = char_index + 26
                plain_char = chr(char_index)
                plaintext += plain_char
            elif ord("A") <= char_index <= ord("Z"):
                char_index = char_index - shift
                if char_index < ord("A"):
                    char_index = char_index + 26
                plain_char = chr(char_index)
                plaintext += plain_char
        else:
            plaintext += element
    return plaintext

# For commit
