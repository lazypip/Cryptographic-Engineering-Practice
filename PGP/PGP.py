"""
TODO : PGP project with sm2 and sm4.
"""

from gmssl import sm2
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT
from pgp_utility import generateKey_128, ECC_DEMO

from typing import *
from pickle import dumps, loads


class PGP_send:
    iv = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

    def __init__(self, pk: str) -> None:
        self.pk = pk  # 对方公钥
    
    def encrypt(self, msg: bytes) -> List[bytes]:
        """TODO : 实现PGP加密方案"""
        # 生成对称密钥
        key: bytes = generateKey_128()
        # msg SM4对称加密
        crypt_sm4 = CryptSM4()
        crypt_sm4.set_key(key, SM4_ENCRYPT)
        encrypt_msg = crypt_sm4.crypt_cbc(PGP_send.iv, msg)

        # key SM2公钥加密
        sm2_crypt = sm2.CryptSM2(public_key=self.pk, private_key=b'\x00')
        encrypt_key = sm2_crypt.encrypt(key)
        self.encrypt_msg = [encrypt_msg, encrypt_key]

        return self.encrypt_msg

    def msgToStream(self, msg) -> bytes:
        """TODO : 序列化"""
        return dumps(msg)


class PGP_recv:
    iv = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

    def __init__(self, rk: str) -> None:
        self.rk = rk  # 本方私钥

    def decrypt(self, encrypt_msg, encrypt_key) -> bytes:
        """TODO : 恢复msg"""
        sm2_crypt = sm2.CryptSM2(public_key=b'\x00', private_key=self.rk)
        decrypt_key = sm2_crypt.decrypt(encrypt_key)

        crypt_sm4 = CryptSM4()
        crypt_sm4.set_key(decrypt_key, SM4_DECRYPT)
        self.decrypt_msg = crypt_sm4.crypt_cbc(PGP_recv.iv, encrypt_msg)

        return self.decrypt_msg

    def streamToMsg(self, msg) -> Any:
        """TODO : 反序列化"""
        return loads(self.msg)



if __name__ == "__main__":
    """ [Alice发送] """
    pk_Bob = ECC_DEMO.public_key
    msg: str = "Hello World"
    print("Original msg:", msg)
    Alice = PGP_send(pk_Bob)
    cipher = Alice.encrypt(msg.encode(encoding='utf-8'))

    """ [Bob接收] """
    rk_Bob = ECC_DEMO.private_key
    Bob = PGP_recv(rk_Bob)
    plain = Bob.decrypt(cipher[0], cipher[1])
    print("Decrypted msg:", plain.decode(encoding='utf-8'))
