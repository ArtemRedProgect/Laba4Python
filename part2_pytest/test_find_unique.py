import pytest
from find_unique import find_unique


@pytest.mark.parametrize("items, expected", [
    ([1, 2, 2, 3, 1, 4], [3, 4]),
    ([], []),
    ([1, 1, 1], []),
    (["a", "b", "a", "c"], ["b", "c"]),
    ([5], [5]),
])
def test_find_unique(items, expected):
    assert find_unique(items) == expected