"""
Definition between Diff and Corresponding Number.
0  zero diff - 0
1* certain nonzero - 1
1  uncertain nonzero - 2
2* (1* ^ 1) - 3
others - 4
Operational rules of xor, function...
"""
diffDict = {0: '0', 1: '1*', 2: '1', 3: '2*', 4: 'others'}
diffDict_reverse = {'0': 0, '1*': 1, '1': 2, '2*': 3, 'others': 4}


def xor(x: int, y: int) -> int:
    """calculate x ^ y """
    if x > y:
        x, y = y, x
    result = {0: [0, 1, 2, 3, 4],
              1: [-1, 4, 3, 4, 4],
              2: [-1, -1, 4, 4, 4],
              3: [-1, -1, -1, 4, 4],
              4: [-1, -1, -1, -1, 4]}
    return result[x][y]


def function(x: int) -> int:
    """value of function(x)"""
    result = [0, 2, 2, 4, 4]
    return result[x]
