import pytest
from count_words import count_words


@pytest.mark.parametrize("sentence, expected", [
    ("hello world", 2),
    ("", 0),
    ("   ", 0),
    ("one", 1),
    ("many   spaces   between words", 4),
    ("  leading and trailing  ", 3),
])
def test_count_words(sentence, expected):
    assert count_words(sentence) == expected