# sm2 2P sign

## Description

​	Alice和Bob均拥有私钥$d_1, d_2$，方案在不交换两方私钥的前提下，使用私钥$d=(d_1d_2)^{-1}-1$对消息进行签名。

Alice需要发送：

- $P1=(d1)^{-1}G$
- $Q1=k_1G$
- $e=hash(msg)$

Bob需要发送：

- $r=(x_1+e) \ mod \ n$
- $s_2=dk_3 \ mod \ n$
- $s_3=d_2(r+k_2) \ mod\ n$



```shell
# 代码可直接运行
python bob.py  # listen
python alice.py
```

## API

Alice要求签名

```python
# 测试数据
msg = b'Hello World'
d1: int = 29961548851145005752492999631966189269019961579632395037624588624422867869608

# [Alice API]
P: hex_t = TpSign.aliceR1(d1)  # 公钥64 bytes
k1 = TpSign.aliceR2(msg)
sign: hex_t = TpSign.aliceR3(d1, k1)
print("Get Signature:", sign)

# Verify the sig
sm2_crypt = sm2.CryptSM2(public_key=P, private_key='00')
msg_hash: hex_t = sm3_hash(bytes_to_list(msg))
msg_hash: bytes = bytes.fromhex(msg_hash)
if sm2_crypt.verify(sign, msg_hash):
    print("Valid Signature")
else:
    print("Wrong Signature")
```

Bob

```python
# 测试数据
d2: int = 31751788944513252796225150725089577150979189460788027183398886939836100929870

# [Bob API]
P: hex_t = TpSign.bobR1(d2)
TpSign.bobR2(d2)
```

## Demo

Alice收到签名并验签

![image-20220730133211275](https://raw.githubusercontent.com/lazypip/readme_pices/main/crypto_pic/image-20220730133211275.png)

