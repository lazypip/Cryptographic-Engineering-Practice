from gmssl.sm2 import default_ecc_table, CryptSM2
from gmssl.sm3 import sm3_hash
from gmssl.func import random_hex, bytes_to_list
from ecc_utility import neg_point, ecc_add

import socket
from sys import exit
from pickle import dumps, loads

from typing import *
hex_t = str  # 16进制字符串

ecc_table = default_ecc_table
ecc_n = int(ecc_table['n'], 16)

alice_addr = ('127.0.0.1', 7777)
bob_addr = ('127.0.0.1', 8888)


class TpSign:
    def generateD() -> int:
        """TODO: 生成私钥"""
        d = random_hex(64)
        return int(d, 16)

    def aliceR1(d1: int) -> hex_t:
        """TODO: alice 第一轮数据计算发送
        ret: 公钥P
        """
        sm2 = CryptSM2('00', '00')

        d_inverse  = TpSign._inverse(d1, 1)
        P1 = sm2._kg(d_inverse, ecc_table['g'])
        TpSign._send(P1, bob_addr)

        # 接收公钥
        P = TpSign._recv(alice_addr)
        return P


    def aliceR2(msg: bytes) -> int:
        """TODO: alice 第二轮数据计算发送
        ret: k1
        """
        e: hex_t = sm3_hash(bytes_to_list(msg))
        k1 = random_hex(64)  # 32 bytes
        k1: int = int(k1, 16) % ecc_n
        
        sm2 = CryptSM2('00', '00')
        Q1 = sm2._kg(k1, ecc_table['g'])

        sendData = [Q1, e]
        TpSign._send(sendData, bob_addr)

        return k1

    
    def aliceR3(d1: int, k1: int) -> hex_t:
        """TODO: alice 第二轮数据计算发送"""
        recvData = TpSign._recv(alice_addr)
        r, s2, s3 = recvData  # int
        s = (d1 * s3 - r) % ecc_n
        tmp = (d1 * k1) % ecc_n
        s: int = (s + tmp * s2) % ecc_n  # 32 bytes

        if s == 0 or s == ecc_n - r:
            print("Wrong signature")
            exit(1)
        r = hex(r)[2:].rjust(64, '0')
        s = hex(s)[2:].rjust(64, '0')

        return r + s



    def bobR1(d2: int) -> hex_t:
        """TODO: bob第一轮数据接收与计算
        ret: 公钥P """
        P1 = TpSign._recv(bob_addr)
        P = TpSign._generateP(d2, P1)
        # 传送公钥
        TpSign._send(P, alice_addr)
        return P

    
    def bobR2(d2: int) -> None:
        """TODO: bob第三轮数据接收与计算"""
        sm2 = CryptSM2('00', '00')

        recvData = TpSign._recv(bob_addr)
        Q1, e = recvData[0], recvData[1]

        k2, k3 = random_hex(64), random_hex(64)  # 32 bytes
        k2, k3 = int(k2, 16) % ecc_n, int(k3, 16) % ecc_n

        Q2 = sm2._kg(k2, ecc_table['g'])
        k3Q1 = sm2._kg(k3, Q1)

        xy: hex_t = ecc_add(Q2, k3Q1)
        x1, y1 = xy[:64], xy[64:]

        r = ( int(x1, 16) + int(e, 16) ) % ecc_n
        s2 = (d2 * k3) % ecc_n
        s3 = (d2 * (r + k2)) % ecc_n

        sendData = [r, s2, s3]
        TpSign._send(sendData, alice_addr)


    def _generateP(d2: int, P1: hex_t) -> hex_t:
        """TODO: 生成公钥P"""
        sm2 = CryptSM2('00', '00')

        d_inv = TpSign._inverse(d2, 1)
        l: hex_t = sm2._kg(d_inv, P1)  # d2^{-1} * P1
        r: hex_t = neg_point(ecc_table['g'])  # -G

        return ecc_add(l, r)
    

    def _inverse(d1: int, d2: int) -> int:
        """TODO : 在n上的逆元"""
        a = (d1 * d2) % ecc_n
        res = pow(a, ecc_n - 2, ecc_n)

        return res
    
    def _send(msg: Any, dst_addr: tuple) -> None:
        """TODO: 发送"""
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msg = dumps(msg)
        client_socket.sendto(msg, dst_addr)


    def _recv(addr: tuple) -> Any:
        """TODO: 接收"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind(addr)
        receive_data, client = server_socket.recvfrom(1024)

        return loads(receive_data)
