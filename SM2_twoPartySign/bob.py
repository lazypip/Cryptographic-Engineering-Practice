from TpSign import TpSign, hex_t

if __name__ == "__main__":
    # 首先进入监听状态
    d2: int = 31751788944513252796225150725089577150979189460788027183398886939836100929870

    P: hex_t = TpSign.bobR1(d2)
    TpSign.bobR2(d2)
