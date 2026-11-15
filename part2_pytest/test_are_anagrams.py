import pytest
from are_anagrams import are_anagrams


@pytest.mark.parametrize("a, b, expected", [
    ("listen", "silent", True),
    ("Listen", "Silent", True),
    ("hello", "world", False),
    ("", "", True),
    ("abc", "abcd", False),
])
def test_are_anagrams(a, b, expected):
    assert are_anagrams(a, b) == expected