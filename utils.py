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
    side = {0: 'top', 1: 'bottom', 2: 'left', 3: 'right', 4: 'inside'}
    values = [0, 0, 0, 0]
    if rect_a.colliderect(rect_b):
        # Check if fully inside
        if rect_a.top <= rect_b.top and \
                rect_a.bottom >= rect_b.bottom and \
                rect_a.left <= rect_b.left and \
                rect_a.right >= rect_b.right:
            return side[4], 0
        # Check each side of the rect
        if rect_a.top <= rect_b.bottom:
            values[0] = abs(rect_a.top - rect_b.bottom)
        if rect_a.bottom >= rect_b.top:
            values[1] = abs(rect_a.bottom - rect_b.top)
        if rect_a.left <= rect_b.right:
            values[2] = abs(rect_a.left - rect_b.right)
        if rect_a.right >= rect_b.left:
            values[3] = abs(rect_a.right - rect_b.left)
        # Return closest side
        index = values.index(min(values))
        return side[index], values[index]
    return None, 0


def rect_above(rect_a, rect_b):
    """
    Returns if a rect is above the other rect
    This also allows if both objects intersect by 1 pixel

    Args:
        rect_a (Rect): The object to check
        rect_b (Rect): The object to check against

    Returns:
        bool: Returns if rect_a is above rect_b
    """
    return rect_a.bottom <= rect_b.top
