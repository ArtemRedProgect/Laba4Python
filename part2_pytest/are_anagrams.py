def are_anagrams(a, b):
    """Проверяет, являются ли две строки анаграммами.

    Args:
        a (str): первая строка.
        b (str): вторая строка.

    Returns:
        bool: True, если строки состоят из одних и тех же букв
              с одинаковым количеством повторений.
    """
    return sorted(a.lower()) == sorted(b.lower())