from gmssl.sm2 import default_ecc_table, CryptSM2
from gmssl.sm3 import sm3_hash
from gmssl.func import random_hex, bytes_to_list
from ecc_utility import neg_point, ecc_add

import socket
from pickle import dumps, loads

from typing import *
hex_t = str  # 16进制字符串


ecc_table = default_ecc_table
ecc_n = int(ecc_table['n'], 16)

class TpDec:
    def generateDK() -> List[int]:
        """TODO : 生成两方私钥"""
        d1, d2 = random_hex(64), random_hex(64)  # 32 bytes
        d1, d2 = int(d1, 16) % ecc_n, int(d2, 16) % ecc_n

        return d1, d2


    def generatePK(d1: int, d2: int) -> hex_t:
        """TODO: 由两方私钥生成公钥"""
        sm2 = CryptSM2('00', '00')
        rk = TpDec._inverse(d1, d2) - 1
        rk: int = rk % ecc_n
        pk: hex_t = sm2._kg(rk, ecc_table['g'])  # 64 byte

        return pk


    def encrypt(msg: hex_t, pk: hex_t) -> List[hex_t]:
        """TODO : pk公钥加密
        msg为32字节块
        ret: C1, C2, C3 (hex_t)"""
        k = random_hex(64)  # 32 bytes
        k: int = int(k, 16) % ecc_n
        sm2 = CryptSM2('00', '00')
        msg = msg.rjust(64, '0')  # 32 bytes

        # C1 = kG = (x1, y1)
        C1: hex_t = sm2._kg(k, ecc_table['g'])
        kP: hex_t = sm2._kg(k, pk)  # 64 bytes
        t: hex_t = kP[3:67]  # 作为简化的KDF函数

        # C2 = M ^ t
        C2: hex_t = TpDec._xorHex_t(msg, t)
        # C3 = H(x2 | M | y2) - sm3
        x2: hex_t = kP[:64]  # 32 bytes
        y2: hex_t = kP[64:]  # 32bytes
        data = x2 + msg + y2
        data: bytes = bytes.fromhex(data)
        C3: hex_t = sm3_hash(bytes_to_list(data))

        return [C1, C2, C3]

    
    def decrypt(d1: int, C: List[hex_t], d2: int) -> hex_t:
        """TODO : 恢复消息
        ret : msg(hex_t)
        """
        C1, C2, C3 = C[0], C[1], C[2]
        sm2 = CryptSM2('00', '00')

        d1_inverse = TpDec._inverse(d1, 1)
        T1 = sm2._kg(d1_inverse, C1)  # T1 = d1^{-1} * C1
        #
        """ 需要传输 0x00 = d1"""
        T2: hex_t = TpDec.generateT2(d2, T1)
        #
        # T2 - C1
        C1_neg = neg_point(C1)
        kP: hex_t = ecc_add(T2, C1_neg)
        x2, y2 = kP[:64], kP[64:]  # 作为简化的KDF函数
        t: hex_t = kP[3:67]

        msg = TpDec._xorHex_t(C2, t)
        # check
        data = x2 + msg + y2
        data: bytes = bytes.fromhex(data)
        u: hex_t = sm3_hash(bytes_to_list(data))
        if u == C3:
            return msg
        
        print("Wrong msg")
        return '00'

    
    def decryptInteract(d1: int, C: List[hex_t], alice_addr: tuple, Bob_addr) -> hex_t:
        """TODO : 恢复消息
        ret : msg(hex_t)
        """
        C1, C2, C3 = C[0], C[1], C[2]
        sm2 = CryptSM2('00', '00')

        d1_inverse = TpDec._inverse(d1, 1)
        T1 = sm2._kg(d1_inverse, C1)  # T1 = d1^{-1} * C1

        """Interaction"""
        TpDec._send(T1, Bob_addr)
        T2 = TpDec._recv(alice_addr)

        # T2 - C1
        C1_neg = neg_point(C1)
        kP: hex_t = ecc_add(T2, C1_neg)
        x2, y2 = kP[:64], kP[64:]  # 作为简化的KDF函数
        t: hex_t = kP[3:67]

        msg = TpDec._xorHex_t(C2, t)
        # check
        data = x2 + msg + y2
        data: bytes = bytes.fromhex(data)
        u: hex_t = sm3_hash(bytes_to_list(data))
        if u == C3:
            return msg
        
        print("Wrong msg")
        return '00'


    def _send(msg: hex_t, dst_addr: tuple) -> None:
        """TODO: 发送T1 / T2"""
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msg = dumps(msg)
        client_socket.sendto(msg, dst_addr)


    def _recv(addr: tuple):
        """TODO: 接收T1 / T2"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind(addr)
        receive_data, client = server_socket.recvfrom(1024)

        return loads(receive_data)


    def generateT2(d2: int, T1: hex_t) -> hex_t:
        """TODO: 由T1得到T2"""
        sm2 = CryptSM2('00', '00')
        d2_inverse: int = TpDec._inverse(d2, 1)
        T2 = sm2._kg(d2_inverse, T1)  # T2 = d2^{-1} * T1
        return T2


    def _inverse(d1: int, d2: int) -> int:
        """TODO : 在n上的逆元"""
        a = (d1 * d2) % ecc_n
        res = pow(a, ecc_n - 2, ecc_n)

        return res

    def _xorHex_t(m1: hex_t, m2: hex_t) -> hex_t:
        """TODO: 32 bytes 16进制串异或"""
        m1_int = int(m1, 16)
        m2_int = int(m2, 16)

        res_int = m1_int ^ m2_int
        return hex(res_int)[2:].rjust(64, '0')



if __name__ == "__main__":
    d1, d2 = TpDec.generateDK()
    pk = TpDec.generatePK(d1, d2)

    msg = 'Hello World'
    msg: hex_t = bytes.hex(msg.encode(encoding='utf-8'))

    C = TpDec.encrypt(msg, pk)

    res: hex_t = TpDec.decrypt(d1, C, d2)
    res = (bytes.fromhex(res)).decode(encoding='utf-8')
    print(res.lstrip('\x00'))
