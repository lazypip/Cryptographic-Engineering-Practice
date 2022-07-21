"""TODO : 对简化的SM3 (256 -> 32 bit) 进行生日攻击"""
"""
j#}&{68X  and  3;7$^ATu
85qN#8'S  and  <?)^bqNA
+tlW,\E"  and  P. JAbz"
5V"\n'tC6  and  X@mH*<5;
Cfv~?]Ru  and  4[SOZc;7
"""

from SM3 import SM3
from string import printable
from typing import *
from random import randint
from time import time
from sys import exit


chrset = printable  # 所有ascii可打印字符
chrset_len = len(chrset)

def generateHash() -> tuple:
    msg = [chrset[randint(0, chrset_len - 1)] for _ in range(8)]
    msg = "".join(msg)
    msg_hash: SM3 = SM3(msg)
    msg_hash = msg_hash.getResult()[2:10]  # 保留 32 bit 10

    return (msg, msg_hash)


def birthAttack():
    hashList = [generateHash() for _ in range(0x10000)]  # 25 s
    print("build hashList")

    for i in range(0x10000):
        msg, msg_hash = generateHash()
        for msg_, msg_hash_ in hashList:
            if msg_hash == msg_hash_:
                print("Found  {}  and  {} .".format(msg, msg_))
        
        if i % 0x1000 == 0:
            print(hex(i), "/ 0x10000 Done")
    print("END")


if __name__ == "__main__":
    while True:
        birthAttack()
