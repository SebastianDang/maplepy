def clamp(n, minn, maxn):
    """
    Clamps n between minn and maxn

    Args:
        n (iterable): Value to clamp
        minn (iterable): Minimum value
        maxn (iterable): Maximum value

    Returns:
        [type]: [description]
    """
    return max(min(maxn, n), minn)
