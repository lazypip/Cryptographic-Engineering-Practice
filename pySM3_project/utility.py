"""
使用bytes作为中间值转换
or for迭代
"""
from typing import *
from re import findall


def str_to_intList(strList) -> List:
    strList: List[str] = findall(r'.{4}', strList)                     # ['abcd', 'efgh', ...]
    strList: List[bytes] = [ele.encode(encoding='utf-8') for ele in strList]    # ['\x00\x00\x00\x00'...]
    intList = [int.from_bytes(ele, byteorder="big", signed=False) for ele in strList]  # [0x00000000, ...]
    return intList


def str_to_bin(string) -> str:
    str_len = len(string)
    string: bytes = string.encode(encoding='utf-8')  # 字节串
    string: int = int.from_bytes(string, byteorder="big", signed=False)  # 整形
    return bin(string)[2:].rjust(str_len * 8, '0')  # 二进制串


def bin_to_intList(binary) -> List:
    binary = findall(r'.{32}', binary)
    intList = [int(ele, 2) for ele in binary]
    return intList


def lshift(x, size, mod = 0x100000000):
    size = size % 32
    left = (x << size) % mod
    right = x >> (32 - size) % mod
    return left ^ right
