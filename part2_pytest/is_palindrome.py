def is_palindrome(value):
    """Проверяет, является ли слово или число палиндромом.

    Args:
        value (str | int): слово или число для проверки.

    Returns:
        bool: True, если значение читается одинаково в обе стороны.
    """
    text = str(value).lower()
    return text == text[::-1]