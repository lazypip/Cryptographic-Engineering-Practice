"""TODO: passwd leaking check"""
from ecc_utility import *
from gmssl.sm3 import sm3_hash
from gmssl.func import bytes_to_list

from pickle import dumps, loads
import socket

from typing import *


# 超参数
mod = 65537  # 素数示例


def generateSig(data: str, a: int, socket: socket.socket, server_addr: tuple) -> int:
    """TODO: 计算(k, v)并发送至server"""
    data_bytes = data.encode(encoding='utf-8')
    h: hex_t = sm3_hash(bytes_to_list(data_bytes))  # 32 bytes 256 bit
    k: hex_t = h[:2]  # 1 bytes
    k = int(k, 16) % 0xff  # Set index

    v = pow(int(h, 16), a, mod)

    sendData = dumps([k, v])
    socket.sendto(sendData, server_addr)

    return h, v


def check(a: int, socket: socket.socket):
    recvData, _ = socket.recvfrom(1024)
    h_ab, S = loads(recvData)

    a_inverse = ex_gcd(a, mod - 1)
    h_b = pow(h_ab, a_inverse, mod)

    for ele in S:
        if ele[2] == h_b:
            print("Found data in Set", ele)
            print("Passwd leaking found")
            return

    print("Non leaking found")


if __name__ == "__main__":
    username = "123456"
    passwd = "12345678"
    data = username + passwd
    a = 0x77  # 私钥

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind(('127.0.0.1', 7777))
    server_addr = ('127.0.0.1', 8888)

    generateSig(data, a, client_socket, ('127.0.0.1', 8888))
    check(a, client_socket)

