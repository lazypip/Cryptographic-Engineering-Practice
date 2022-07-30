# PGP scheme with sm2

## Description

​	PGP加密方案，使用对称密钥加密数据，使用对方公钥加密对称密钥。将$enc_k(data),enc_{pk}(k)$发送至接收方。

```
# 代码可直接运行
python PGP.py
```

## API

```python
""" [Alice发送] """
pk_Bob = ECC_DEMO.public_key
msg: str = "Hello World"
print("Original msg:", msg)
# [Alice API]
Alice = PGP_send(pk_Bob)
cipher = Alice.encrypt(msg.encode(encoding='utf-8'))

""" [Bob接收] """
rk_Bob = ECC_DEMO.private_key
# [Bob API]
Bob = PGP_recv(rk_Bob)
plain = Bob.decrypt(cipher[0], cipher[1])
print("Decrypted msg:", plain.decode(encoding='utf-8'))
```

## Demo

![image-20220730131928638](https://raw.githubusercontent.com/lazypip/readme_pices/main/crypto_pic/image-20220730131928638.png)

