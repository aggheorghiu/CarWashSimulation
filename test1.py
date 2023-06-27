from typing import List
import doctest

#
# def count_zeros(I: List[int])-> int:
#     """
#     Numara zerourile
#     :param I:
#     :return:
#     >>>[count_zeros([0,1])]
#     1
#     """
#     counter: int = 0
#     for item in I:
#         if item == 0:
#             counter += 1
#         return counter


def factorial(num:int) -> int:
    """

    :param num:
    :return:
    >>> [factorial(i) for i in range(5)]
    [1, 1, 2, 6, 24]
    >>> [factorial(-1)]
    >>> for i in range(5)
    ... factorial(i)
    1
    1
    2
    6
    24
    Traceback (most recent call last):
    ValueError: num must be >= 0
    """
    if num>=0:
        res:int = 1
        for i in range(2, num+1):
            res *= i
        return res
    else:
        raise ValueError("nu e bine")


if __name__:
    import doctest
    doctest.testmod()