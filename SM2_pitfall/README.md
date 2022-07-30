# Verify the sm2 pitfalls with poc code

## Description

​	当SM2密钥泄露会重用时，根据$d_A = \frac{(s_2-s_1)}{s_1-s_2+r_1-r_2} mod\ n$，可直接计算出私钥$d_A$。

```
# 代码可直接运行
python Kreusing.py
python Kleaking.py
```

## API

```python
# 生成测试数据
private_key = 'B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6'\
             '994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
data = b"Hello World"

sm2_crypt = sm2.CryptSM2(public_key=public_key, private_key=private_key)
k: hex_t = func.random_hex(sm2_crypt.para_len)
sign: hex_t = sm2_crypt.sign(data, k)  # 64 bytes
# -------------------------------------------
# [Kleaking API]
d = Kleaking(k, sign)
if d == private_key.lower():
    print("Get private key:", d)

# [kreusing API]
sign_a = sm2_a.sign(data_a, k)  # 获取签名
d_a = Kreusing(k, sign_a)
```

## Demo

k-reusing：
![image-20220730125502537](https://raw.githubusercontent.com/lazypip/readme_pices/main/crypto_pic/image-20220730125502537.png)

k-leaking

![image-20220730125618782](https://raw.githubusercontent.com/lazypip/readme_pices/main/crypto_pic/image-20220730125618782.png)

