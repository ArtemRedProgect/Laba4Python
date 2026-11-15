import pytest
from combine_dicts import combine_dicts


@pytest.mark.parametrize("d1, d2, expected", [
    ({"a": 1, "b": 2}, {"b": 3, "c": 4}, {"a": 1, "b": 3, "c": 4}),
    ({}, {"a": 1}, {"a": 1}),
    ({"a": 1}, {}, {"a": 1}),
    ({}, {}, {}),
])
def test_combine_dicts(d1, d2, expected):
    assert combine_dicts(d1, d2) == expected


def test_combine_dicts_does_not_mutate_originals():
    d1 = {"a": 1}
    d2 = {"b": 2}
    combine_dicts(d1, d2)
    assert d1 == {"a": 1}
    assert d2 == {"b": 2}

def test_combine_dicts_preserves_key_order():
    d1 = {"a": 1, "b": 2}
    d2 = {"b": 3, "c": 4}

    result = combine_dicts(d1, d2)

    assert list(result.keys()) == ["a", "b", "c"]