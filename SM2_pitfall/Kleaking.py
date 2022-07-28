"""TODO: SM2 signature leaking k"""
from ecc_utility import *
from gmssl import sm2, func


def Kleaking(k: hex_t, sign: hex_t) -> hex_t:
    """TODO: compute rk through k, sig"""
    r, s = sign[:64], sign[64:]
    k: int = int(k, 16)
    r: int = int(r, 16)
    s: int = int(s, 16)
    d: int = (k - s) % ecc_n
    d: int = (d * inverse(r + s, 1)) % ecc_n

    return hex(d)[2:].rjust(64, '0')


if __name__ == "__main__":
    private_key = 'B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
    public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6'\
                 '994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
    data = b"Hello World"
    
    sm2_crypt = sm2.CryptSM2(public_key=public_key, private_key=private_key)
    k: hex_t = func.random_hex(sm2_crypt.para_len)

    sign: hex_t = sm2_crypt.sign(data, k)  # 64 bytes
    d = Kleaking(k, sign)
    if d == private_key.lower():
        print("Get private key:", d)
    else:
        print("Fail")
