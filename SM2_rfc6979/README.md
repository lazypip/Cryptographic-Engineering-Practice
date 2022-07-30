

# Impl sm2 with RFC6979

## Description

​	由于使用相同的k会导致私钥泄露，因此使用RFC6979的过程生成sm2的随机数k，使k由明文M，公钥pk生成。从而避免k的重用。

```
# 代码可直接运行
python RFC6979.py
```

## API

```python
# 测试数据
rk: hex_t = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
pk: hex_t = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6' \
            '994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'

msg1 = b'Hello World'
print('Msg: ', msg1)
# [API]
SM2rfc6979(msg1, rk, pk)

msg2 = b'Qing dao'
print('Msg: ', msg2)
SM2rfc6979(msg2, rk, pk)
```

## Demo

![image-20220730180759341](https://raw.githubusercontent.com/lazypip/readme_pices/main/crypto_pic/image-20220730180759341.png)

## Refer

https://www.rfc-editor.org/rfc/inline-errata/rfc6979.html