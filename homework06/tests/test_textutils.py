import pytest

import textutils


def test_clean() -> None:
    assert textutils.clean("A.b,(c)") == "Abc"
