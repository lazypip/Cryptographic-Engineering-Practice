"""
TODO : ECC functions for utility.
"""
from gmssl.sm2 import CryptSM2
from typing import *

hex_t = str

default_ecc_table = {
    'n': 'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123',
    'p': 'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF',
    'g': '32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7'\
         'bc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0',
    'a': 'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC',
    'b': '28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93',
}
ecc_n = int(default_ecc_table['n'], 16)


def legendre_symbol(a, p):
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls


def modular_sqrt(a, p):
    """TODO : 计算二次剩余"""
    if legendre_symbol(a, p) != 1:
        return 0
    elif a == 0:
        return 0
    elif p == 2:
        return p
    elif p % 4 == 3:
        return pow(a, (p + 1) // 4, p)

    s = p - 1
    e = 0
    while s % 2 == 0:
        s //= 2
        e += 1

    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1
    x = pow(a, (s + 1) // 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e

    while True:
        t = b
        m = 0
        for m in range(r):
            if t == 1:
                break
            t = pow(t, 2, p)

        if m == 0:
            return x

        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m


def neg_point(P1):
    """ hex -> hex
    -(x, y) = (x, p - y) , 32 bytes + 32 bytes"""
    p = int(default_ecc_table['p'], 16)  # 32 bytes
    x = P1[:64]  # 32 bytes
    y = int(P1[64:], 16)
    y = hex(p - y)[2:]

    return x + y


def gcd(a,b):
    """TODO : 欧几里得算法求最大公因子"""
    if a < b:
        a, b = b, a
    while (b!=0):
        a, b = b, a % b
    return a


def ex_gcd(a,m=ecc_n):
    """TODO : 应用扩展欧几里得 由于(a,m)=1时，有ax+bm=1，即ax = 1(mod m) x即为逆元"""
    if gcd(a,m)==0:
        print("Error")
        return
    a = a % m  # 减少运算量
    
    # 需要两个等式以构建下一个等式
    n1, n2, n3 = 1, 0, a
    n1_, n2_, n3_ = 0, 1, m
    while n3_ != 0:
        q = n3 // n3_   # 使等式右边为余数并递减
        n1_, n2_, n3_, n1, n2, n3 = n1 -q * n1_, n2 - q * n2_, n3 - q * n3_, n1_, n2_, n3_

    return n1 % m   # 化为最小


def ecc_add(P1: str, P2: str) -> str:
    """
    TODO : 实现ECC加法
    para : hex, ret : hex
    """
    P1 = [int(P1[:64], 16), int(P1[64:], 16)]
    P2 = [int(P2[:64], 16), int(P2[64:], 16)]

    if P1[0] > P2[0]:
        P1, P2 = P2, P1

    res = [0, 0]
    mod = int(default_ecc_table['p'], 16)
    tt = (P2[1] - P1[1]) * ex_gcd(P2[0] - P1[0], mod) % mod

    res[0] = (pow(tt, 2) - P1[0] - P2[0]) % mod
    res[1] = (tt * (P1[0] - res[0]) - P1[1]) % mod

    return hex(res[0])[2:].rjust(64, '0') + hex(res[1])[2:].rjust(64, '0')


def ecc_kg(k: int, point=default_ecc_table['g']) -> hex_t:
    """TODO: 借用gmssl点乘"""
    sm2 = CryptSM2('00', '00')
    return sm2._kg(k, point)
