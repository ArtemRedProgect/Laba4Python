def find_unique(items):
    """Возвращает элементы, встречающиеся в списке ровно один раз.

    Args:
        items (list): исходный список.

    Returns:
        list: элементы, встретившиеся ровно один раз, в порядке
              их первого появления.
    """
    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return [item for item in items if counts[item] == 1]