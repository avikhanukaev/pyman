def vector_addition(v1, v2):
    """
    This function performs linear algebra vector addition. For example, if
    v1 = [2, 3], v2 = [1, 1] then v1 + v2 = [2+1, 3+1]= [3, 4]

    Important note: It is important that v1 and v2 have same dimension (len).

    :param v1: list of numbers
    :param v2: list of number
    :return: The summation of the vectors.
    """
    result = []
    for i in range(len(v1)):
        result.append(v1[i] + v2[i])
    return result


def get_orientation(source, target):
    """
    This function returns the orientation of movement. For example, if we
    currently stand on point [2, 3] and we move to [2, 4], then it means that
    we move left.

    It is important to note that the [0, 0] point is the top left button and
    that the first entry is the vertical, while the second entry is the
    horizontal.

    :param source: list of two number denote the current point we stand on.
    :param target: list of two number denote the target point.
    :return: One of ['left', 'right', 'down', 'up'] directions. It returns
    'None' otherwise.
    """
    if vector_addition(source, [0, 1]) == target:
        return 'right'
    elif vector_addition(source, [0, -1]) == target:
        return 'left'
    elif vector_addition(source, [1, 0]) == target:
        return 'down'
    elif vector_addition(source, [-1, 0]) == target:
        return 'up'
    return 'None'
