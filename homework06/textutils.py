import string


def clean(s: str) -> str:
    """ Clear punctuation marks from text """
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)
