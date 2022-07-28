"""TODO : 对简化的SM3 (256 -> 32 bit) rho碰撞"""

from SM3 import SM3

from string import printable
from random import randint

from sys import exit
from typing import *


chrset = printable  # 所有ascii可打印字符
chrset_len = len(chrset)


def generateHash() -> List:
    msg = [chrset[randint(0, chrset_len - 1)] for _ in range(8)]
    msg = "".join(msg)
    msg_hash: SM3 = SM3(msg)
    msg_hash = msg_hash.getResult()[2:10]  # 保留 32 bit

    return msg, msg_hash

def rhoAttack() -> List:
    """TODO: 寻找环形碰撞"""
    msg, msg_hash = generateHash()
    msg_list = [msg,]
    hash_list = [msg_hash, ]
    found_signal = False
    colli_index = 0
    while not found_signal:
        msg, msg_hash = generateHash()
        if msg_hash in hash_list:
            print("Found collision")
            colli_index = hash_list.index(msg_hash)
            found_signal = True

        msg_list.append(msg)
        hash_list.append(msg_hash)

    return msg_list, hash_list, colli_index


if __name__ == "__main__":
    msg, hash, index = rhoAttack()
    print(msg, hash, index, end='\n')
