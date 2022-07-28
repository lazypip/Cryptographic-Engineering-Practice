"""TODO: ECDSH: Forge signature 
         when the msg is not checked.
         (with sm2 ecc_table)
"""
from gmssl.sm3 import bytes_to_list, sm3_hash
from gmssl.func import random_hex

from ecc_utility import *

from typing import *


def forge(pk: hex_t) -> List[hex_t]:
    """TODO: forge signature when msg is not check"""
    u: int = int(random_hex(64), 16) % ecc_n
    v: int = int(random_hex(64), 16) % ecc_n
    uG = ecc_kg(u)
    vP = ecc_kg(v, pk)
    R = ecc_add(uG, vP)
    x: hex_t = R[:64]

    r: int = int(x, 16) % ecc_n

    v_inv = ex_gcd(v)
    e = (r * u * v_inv) % ecc_n
    s = (r * v_inv) % ecc_n

    sign_new = hex(r)[2:].rjust(64, '0') + hex(s)[2:].rjust(64, '0')
    e = hex(e)[2:].rjust(64, '0')

    return e, sign_new



def ecdshSign(msg: bytes, rk: hex_t) -> hex_t:
    k: hex_t = random_hex(64)  # 32 bytes
    k = int(k, 16) % ecc_n
    R = ecc_kg(k)
    r = R[:64]

    e: hex_t = sm3_hash(bytes_to_list(msg))  # 32 bytes
    k_inv = ex_gcd(k)
    s = (int(e, 16) + int(rk, 16) * int(r, 16)) % ecc_n
    s: int = (k_inv * s) % ecc_n

    s: hex_t = hex(s)[2:].rjust(64, '0')

    return r + s


def ecdshVerify(msg: bytes, pk: hex_t, sign, hash=None) -> bool:
    if hash:
        e: hex_t = hash  # 若输入hash, 则不检测消息
    else:
        e: hex_t = sm3_hash(bytes_to_list(msg))  # 32 bytes

    r, s = sign[:64], sign[64:]
    w: int = ex_gcd(int(s, 16))

    rwP: hex_t = ecc_kg((int(r, 16) * w) % ecc_n, point=pk)
    ewG = ecc_kg((int(e, 16) * w) % ecc_n)
    r_s = ecc_add(rwP, ewG)
    r_new: hex_t = r_s[:64].lower()

    if r.lower() == r_new:
        print("Valid sign")
        return True
    else:
        print("Invalid sign")
        return False


if __name__ == "__main__":
    rk = 'B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
    pk = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A8308'\
         '1A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
    
    msg = b'Hello World'
    # sign = ecdshSign(msg, rk)
    # ecdshVerify(msg, pk, sign)

    e, sign = forge(pk)
    ecdshVerify(msg, pk, sign, e)
