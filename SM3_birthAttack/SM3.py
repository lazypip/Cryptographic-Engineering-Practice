from typing import *
from utility import *
from sys import exit
from math import ceil


class SM3_Utility:
    # msg for test
    msg_test = "abcd" * 64
    msg256_test = 'A' * 256
    msg512_test = 'B' * 512
    msg768_test = 'C' * 768

    IV = [  0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600,
            0xa96f30bc, 0x163138aa, 0xe38dee4d, 0xb0fb0e4e  ]  # 32bit * 8 = 256bits

    def T(i) -> int:
        if i < 16:
            return 0x79cc4519
        return 0x7a879d8a

    def FF(x, y, z, i) -> int:
        if i < 16:
            return x ^ y ^ z
        else:
            return (x & y) | (x & z) | (y & z)
    
    def GG(x, y, z, i) -> int:
        if i < 16:
            return x ^ y ^ z
        else:
            return (x & y) | (~x & z)

    def P0(x):
        return x ^ lshift(x, 9) ^ lshift(x, 17)

    def P1(x):
        return x ^ lshift(x, 15) ^ lshift(x, 23)


class SM3:
    def _tmpValue(self):
        """TODO : 存储中间值"""
        self.preInput = SM3_Utility.IV  # 256 bit
        self.msg_ptr = -1            # 模拟文件指针
        self.msg_signal = False     # normal Block 结束标识

        
    def __init__(self, msg: str) -> None:
        self.msg = msg
        self.msg_len = len(msg) * 8  # bit长度
        self.group_mod = self.msg_len % 512
        self.group_size = ceil((self.msg_len) / 512) - 1  # final block index

        self._tmpValue()


    def _getNextBlock(self) -> List:
        """ TODO : 获取下一BLOCK 并将其转换为列表的形式
        curBloc <- [0xffffffff, 0xffffffff, ...] 共 512 / 32 = 16 个元素 """
        self.msg_ptr += 1
        # final block
        if self.msg_ptr == self.group_size:
            self.msg_signal = True
            return self._getFinalBlock()

        """next normal block"""
        startOffset = self.msg_ptr * (512 // 8)
        nextBlock: str = self.msg[startOffset : startOffset + 512 // 8]
        return str_to_intList(nextBlock)  # 将 string 转换为 16 * 32 bit int列表


    def _getFinalBlock(self) -> List:
        len_padding = bin(self.msg_len)[2:].rjust(64, '0')

        startoff = self.msg_ptr * (512 // 8)
        finalBlock_str = self.msg[startoff:]
        assert len(finalBlock_str) * 8 % 512 == self.group_mod

        finalBlock_bin = str_to_bin(finalBlock_str) + '1'  # 填充二进制串
        if len(finalBlock_bin) + 64 > 512:
            zero_padding = '0' * (512 * 2 - len(finalBlock_bin) - 64)
            finalBlock = bin_to_intList(finalBlock_bin + zero_padding + len_padding)
            res = [finalBlock[:16], finalBlock[16:]]
            return res
        else:
            zero_padding = '0' * (512 - len(finalBlock_bin) - 64)
            finalBlock = bin_to_intList(finalBlock_bin + zero_padding + len_padding)
            return finalBlock


    def _update(self, curBlock: List[int]):
        """TODO: 消息扩展、压缩函数"""
        pre = self.preInput[::]        #  8 * 32 = 256 bit
        curBlock_512 = curBlock        # 16 * 32 = 512 bit

        """ [消息扩展 W] """
        W_68 = curBlock_512 + [0x00 for _ in range(52)]
        assert len(W_68) == 68
        for j in range(16, 68):
            W_68[j] = W_68[j - 6] ^ lshift(W_68[j-13], 7)
            tmp = W_68[j - 16] ^ W_68[j - 9] ^ lshift(W_68[j - 3], 15)
            tmp = SM3_Utility.P1(tmp)
            W_68[j] ^= tmp

        """ [消息扩展 WW] """
        WW_64 = [0x00 for _ in range(64)]
        for j in range(0, 64):
            WW_64[j] = W_68[j] ^ W_68[j + 4]

        """ [压缩函数] """
        for j in range(0, 64):
            SS1 = ( lshift(pre[0], 12) + pre[4] + lshift(SM3_Utility.T(j), j) ) % 0x100000000
            SS1 = lshift(SS1, 7)
            SS2 = SS1 ^ lshift(pre[0], 12)
            TT1 = ( SM3_Utility.FF(pre[0], pre[1], pre[2], j) + pre[3] + SS2 + WW_64[j] ) % 0x100000000
            TT2 = ( SM3_Utility.GG(pre[4], pre[5], pre[6], j) + pre[7] + SS1 + W_68[j]  ) % 0x100000000

            pre[3], pre[2] = pre[2], lshift(pre[1], 9)
            pre[1], pre[0] = pre[0], TT1
            pre[7], pre[6] = pre[6], lshift(pre[5], 19)
            pre[5], pre[4] = pre[4], SM3_Utility.P0(TT2)

        self.preInput = list(map(lambda x, y: x ^ y, self.preInput, pre))  #  8 * 32 = 256 bit


    def _final(self, finalBlock):
        """TODO: 填充并处理最后一个模块"""
        if len(finalBlock) == 2:
            self._update(finalBlock[0])
            self._update(finalBlock[1])
        else:
            self._update(finalBlock)
        self.msg_signal = True


    def getResult(self):
        """TODO : """
        while True:
            nextBlock = self._getNextBlock()
            if self.msg_signal:
                self._final(nextBlock)
                break
            self._update(nextBlock)
            
        
        result: List[int] = self.preInput  # 8 * 32 = 256 bit
        result = "".join([hex(ele)[2:].rjust(8, '0') for ele in result])

        # print("SM3 Result : ", "0x" + result)
        return "0x" + result


if __name__ == "__main__":
    hash = SM3(SM3_Utility.msg_test)
    hash.getResult()
