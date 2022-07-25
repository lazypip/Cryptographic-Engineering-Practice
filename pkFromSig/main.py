from gmssl import func, sm2
from gmssl.sm2 import default_ecc_table
from utility import modular_sqrt, neg_point, ecc_add


def getPK(R: int, S: int, data: bytes, sm2_obj: sm2) -> None:
    """
    TODO : get SM2 pk from (R, S) and msg.
    """
    pk = [0, 0]

    # (s + r) ^{-1} mod n
    r_1 = pow(S + R, int(default_ecc_table['n'], base=16) - 2, int(default_ecc_table['n'], base=16))  # 求逆

    # kG
    r_2 = []
    x = ( R - int(data.hex(), 16) ) % int(default_ecc_table['n'], 16)
    Dy = pow(x, 3, int(default_ecc_table['p'], 16)) \
            + (int(default_ecc_table['a'], 16) * x ) % int(default_ecc_table['p'], 16) \
            + int(default_ecc_table['b'], 16)

    Dy %= int(default_ecc_table['p'], 16)
    y = modular_sqrt(Dy, int(default_ecc_table['p'], 16))
    r_2.append(hex(x)[2:].rjust(64, '0') + hex(y)[2:].rjust(64, '0'))

    y = (int(default_ecc_table['p'], 16) - y) % int(default_ecc_table['p'], 16)
    r_2.append(hex(x)[2:].rjust(64, '0') + hex(y)[2:].rjust(64, '0'))

    # -sG
    r_3 = neg_point(default_ecc_table['g'])
    r_3 = sm2_obj._kg(S, r_3)  # -sG

    # kG - sG
    r_4 = [0, 0]
    r_4[0] = ecc_add(r_2[0], r_3)
    pk[0] = sm2_obj._kg(r_1, r_4[0])  # 64 byte

    r_4[1] = ecc_add(r_2[1], r_3)
    pk[1] = sm2_obj._kg(r_1, r_4[1])  # 64 byte

    print("The protential pk:", pk[0], '\n or ', pk[1])


if __name__ == "__main__":
    # 32 bytes
    private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
    # 64 bytes
    public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6'\
                '994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'

    data = b"111"
    sm2_crypt = sm2.CryptSM2(public_key=public_key, private_key=private_key)
    R_S = sm2_crypt.sign(data, func.random_hex(sm2_crypt.para_len))

    # 恢复公钥
    R, S = int(R_S[:64], 16), int(R_S[64:], 16)
    getPK(R, S, data, sm2_crypt)
