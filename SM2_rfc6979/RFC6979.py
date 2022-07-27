from hashlib import sha256
from hmac import new
from gmssl import sm2


hex_t = str


def SM2rfc6979(msg: bytes, rk: hex_t, pk: hex_t) -> hex_t:
    """TODO : 
        根据RFC6979 改进k生成过程
        避免k重用导致rk泄露
    """
    sm2_crypt = sm2.CryptSM2(rk, pk)
    k = generateK(msg, rk)
    sign: hex_t = sm2_crypt.sign(msg, k)
    print("Generated k: ", k)
    print("DSA: ", sign)

    return k, sign


def generateK(msg: bytes, rk: hex_t) -> hex_t:
    """TODO: 根据RFC6979生成sm2 k mod n
    k - 32 bytes
    hash - sha256
    """
    # a
    h1: hex_t = getHash(msg)
    # b
    V: hex_t = '01' * 32  # 32 bytes
    # c
    K: hex_t = '00' * 32
    # d
    data: hex_t = V + '00' + rk + h1
    K: hex_t = getHmac(K, data)
    # e
    V: hex_t = getHmac(K, V)
    # f
    data: hex_t = V + '01' + rk + h1
    K = getHmac(K, data)
    # g
    V = getHmac(K, V)
    # h
    T: hex_t = ""
    tlen = 0
    while tlen < 64:
        V = getHmac(K, V)
        T = T + V
        tlen = len(T)
    
    k: hex_t = T[:64]
    n: hex_t = sm2.default_ecc_table['n']
    k_int = int(k, 16) % int(n, 16)

    return hex(k_int)[2:].rjust(64, '0')
    

def getHash(x: bytes) -> hex_t:
    """TODO: sha256"""
    return sha256(x).hexdigest()


def getHmac(key: hex_t, data: hex_t) -> hex_t:
    """TODO : sha256 Hmac"""
    key = bytes.fromhex(key)
    data = bytes.fromhex(data)

    obj = new(key, data, digestmod='sha256')
    return obj.hexdigest()


if __name__ == "__main__":
    rk: hex_t = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
    pk: hex_t = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6' \
                '994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'

    msg1 = b'Hello World'
    print('Msg: ', msg1)
    SM2rfc6979(msg1, rk, pk)

    msg2 = b'Qing dao'
    print('Msg: ', msg2)
    SM2rfc6979(msg2, rk, pk)
