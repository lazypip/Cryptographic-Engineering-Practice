"""TODO: SM2 signature reusing k"""
from ecc_utility import *
from gmssl import sm2, func
import ecdsa.ecdsa


def Kreusing(k: hex_t, sign: hex_t) -> hex_t:
    """TODO: SM2 signature reusing k"""
    r, s = sign[:64], sign[64:]
    k: int = int(k, 16)
    r: int = int(r, 16)
    s: int = int(s, 16)
    d: int = (k - s) % ecc_n
    d: int = (d * inverse(r + s, 1)) % ecc_n

    return hex(d)[2:].rjust(64, '0')



if __name__ == "__main__":
    rk_a = 'B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'.lower()
    pk_a = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6'\
           '994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
    
    rk_b = '7ae40b13c8417980feb726e6d955f5b853abe21413061ceea66388121d9a0353'
    pk_b = '83309e429d20e82ec19f3d3f1f9b11abf33d6327daf3589bb667d3e6c666df258699'\
           '32bfa27a951cf30ca959bd4bfc8e13dbbf9bd92de73707b0e97aee369cdb'

    k: hex_t = func.random_hex(64)  # 32 bytes
    data_a, data_b = b"Hello", b"World"

    sm2_a = sm2.CryptSM2(public_key=pk_a, private_key=rk_a)
    sm2_b = sm2.CryptSM2(public_key=pk_b, private_key=rk_b)

    sign_a = sm2_a.sign(data_a, k)
    sign_b = sm2_b.sign(data_b, k)

    d_b = Kreusing(k, sign_b)
    d_a = Kreusing(k, sign_a)

    print(d_b, d_a)
