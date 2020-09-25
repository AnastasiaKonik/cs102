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
        shift = ord((shift_alpha).lower()) - ord('a')
        if element.isalpha() != 0 and shift != 0:
            a = ord(element)
            if a >= 97 and a <= 122:
                a = a + shift
                if a > 122:
                    a = a - 26
                b = chr(a)
                ciphertext += b
            elif a >= 65 and a <= 90:
                a = a + shift
                if a > 90:
                    a = a - 26
                b = chr(a)
                ciphertext += b
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
        shift = ord((shift_alpha).lower()) - ord('a')
        if element.isalpha() != 0 and shift != 0:
            a = ord(element)
            if a >= 97 and a <= 122:
                a = a - shift
                if a < 97:
                    a = a + 26
                b = chr(a)
                plaintext += b
            elif a >= 65 and a <= 90:
                a = a - shift
                if a < 65:
                    a = a + 26
                b = chr(a)
                plaintext += b
        else:
            plaintext += element
    return plaintext
#For commit