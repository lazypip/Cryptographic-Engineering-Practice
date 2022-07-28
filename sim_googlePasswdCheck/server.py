"""TODO: 存储社工库, 返回相应集合"""
from ecc_utility import *
from gmssl.sm3 import sm3_hash
from gmssl.func import bytes_to_list

from random import randint
from pickle import dumps, loads
import socket

from string import hexdigits
from typing import *


# 超参数
mod = 65537


def generateDict(b: int, num: int = 2**10) -> List[List]:
    """TODO: 随机生成示例社工列表
    ret: 按照k_i分成2^{8}组
    """
    setLen = len(hexdigits)
    randFunc = lambda x: ''.join([hexdigits[randint(0, setLen - 1)] for _ in range(x)])  # 生成x位字符串

    dataList = [[] for _ in range(0xff)]  # 存储0xff组数据
    for i in range(num):
        # 生成
        username: str = randFunc(6)
        passwd: str = randFunc(8)

        if i == 0:  # demo
            username = "123456"
            passwd = "12345678"

        # 计算gruop num
        tmp: bytes = (username + passwd).encode(encoding='utf-8')
        h: hex_t = sm3_hash(bytes_to_list(tmp))  # 32 bytes 256 bit
        k: hex_t = h[:2]  # 1 bytes
        k = int(k, 16) % 0xff

        # 计算v (离散对数)
        v = pow(int(h, 16), b, mod)
        data = (username, passwd, v)
        dataList[k].append(data)
    
    print("DataBase Complete.")
    return dataList  # len(dataList) = 0xff


def reply(b: int, dataList: List, server_addr: tuple) -> None:
    """TODO: 接收(k, v), 发送h^{ab}, set S"""
    # UDP数据接收
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(server_addr)
    receive_data, client = server_socket.recvfrom(1024)

    # 计算
    k, v = loads(receive_data)
    h_ab, S = findDataSet(dataList, b, [k, v])

    # 数据回送
    msg = dumps([h_ab, S])
    server_socket.sendto(msg, client)

    print("Finish one check")


def findDataSet(dataList: List, b: int, recv_data: List) -> List:
    """TODO: 发送h^{ab}, set S"""
    set_num = 0xff
    k, v = recv_data
    
    h_ab = pow(v, b, mod)
    potential_set: List = dataList[k]

    return h_ab, potential_set


if __name__ == "__main__":
    #数据和加密后数据为bytes类型
    b = 0xf7  # 简化私钥

    dataList = generateDict(b)
    server_addr = ('127.0.0.1', 8888)

    while True:
        reply(b, dataList, server_addr)
