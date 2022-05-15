"""retain the replacement for all rounds"""
from operationalRule import *


def oneRoundEncrypt(mL: list, mR: list):
    """(mL || mR) = (x1 || x2 || y1 || y2)"""
    x1, x2 = mL
    y1, y2 = mR
    # f function
    y1, y2 = function(y1), function(y2)
    z1, z2 = xor(x1, y1), xor(x2, y2)
    # linear conversion
    cL = mR
    cR = [z1, z2]
    return cL, cR


def oneRoundDecrypt(cL: list, cR: list):
    """(cL || cR) = (x1 || x2 || y1 || y2)"""
    x1, x2 = cL
    y1, y2 = cR
    # f function
    x1, x2 = function(x1), function(x2)
    z1, z2 = xor(x1, y1), xor(x2, y2)
    # linear conversion
    mR = cL
    mL = [z1, z2]
    return mL, mR


def getDiffChain(L: list, R: list, operation: bool) -> list:
    """stop at (L, R) == (??, ??) == ([4, 4], [4, 4])
        operation 0 for encryption 1 for decryption
        chain[0] for mL, mR for encryption
        chain[0] for cL, cR for Decryption
        """
    chain = [(L, R), ]  # element form [[x1, xy], [y1, y2]]
    functionChoice = oneRoundEncrypt
    if operation:
        functionChoice = oneRoundDecrypt
    while True:
        L, R = functionChoice(L, R)
        chain.append((L, R))
        if L == [4, 4] and R == [4, 4]:
            break
    return chain
