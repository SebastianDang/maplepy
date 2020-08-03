import pygame


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


def colliderect_info(rect_a, rect_b):
    """
    Returns information about the collision

    Args:
        rect_a (Rect): The object to check for collision
        rect_b (Rect): The object collided with

    Returns:
        str, int: Returns the direction and magnitude of collision
    """
    side = {0: 'top', 1: 'bottom', 2: 'left', 3: 'right'}
    values = [0, 0, 0, 0]
    if rect_a.colliderect(rect_b):
        if rect_a.top <= rect_b.bottom:
            values[0] = abs(rect_a.top - rect_b.bottom)
        if rect_a.bottom >= rect_b.top:
            values[1] = abs(rect_a.bottom - rect_b.top)
        if rect_a.left <= rect_b.right:
            values[2] = abs(rect_a.left - rect_b.right)
        if rect_a.right >= rect_b.left:
            values[3] = abs(rect_a.right - rect_b.left)
        index = values.index(min(values))
        return side[index], values[index]
    return None, None
