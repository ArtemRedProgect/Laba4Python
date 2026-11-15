import pytest
from is_palindrome import is_palindrome


@pytest.mark.parametrize("value, expected", [
    ("level", True),
    ("Level", True),
    ("hello", False),
    (121, True),
    (123, False),
    ("", True),
    ("a", True),
])
def test_is_palindrome(value, expected):
    assert is_palindrome(value) == expected