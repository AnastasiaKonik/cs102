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
    for x in plaintext:
        if x.isalpha() != 0:
            a = ord(x)
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
            ciphertext += x
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
    for x in ciphertext:
        if x.isalpha() != 0:
            a = ord(x)
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
            plaintext += x
    return plaintext
