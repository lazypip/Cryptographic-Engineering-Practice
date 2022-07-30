"""TODO : SM3长度扩展攻击"""
from SM3 import SM3
from typing import *


def SM3_extend(extend_msg: str, prehash: List[int]) -> None:
    extend_msg_len = len(extend_msg)
    padding_1 = b''
    extend_msg = extend_msg
    padding_2 = b''
    whole_msg = b''  # padding_1 || msg || padding_2

    """ [输出hash(M || padding_1 || extend_msg || padding_2)] """
    hash = SM3(extend_msg, IV = prehash)
    print(hash.getResult())


if __name__ == "__main__":
    prehash: SM3 = SM3("abcd")
    prehash = prehash.getResult(hexdig=False)

    extend_msg = "efgh"
    print("hash(abcd):", prehash)
    print("hash(abcd | padding | efgh): ")
    SM3_extend(extend_msg, prehash)
