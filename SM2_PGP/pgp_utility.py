from random import randint
from string import printable
from typing import *

table_len = len(printable)

class ECC_DEMO:
    # 32 bytes - 256bit
    private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
    # 64 bytes - 512bit
    public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6' \
                 '994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'


def generateKey_128() -> bytes:
    """TODO : 生成128 bit密钥 - 16 char"""
    key = []
    for _ in range(16):
        rchar = printable[randint(0, table_len - 1)]
        key.append(rchar)

    key = "".join(key)
    key = key.encode(encoding='utf-8')
    return key


if __name__ == "__main__":
    res = generateKey_128()
    print(res)
