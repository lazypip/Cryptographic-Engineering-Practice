# Deduce public key from signature

## Description

​	在没有额外空间存储公钥时，根据$d_AG = P_A = (s+r)^{-1}(kG-sG)$，可直接通过签名值$(r, s)$计算出公钥$P_A$。而由于椭圆曲线的对称性，会计算出两个公钥值，因此仍需1bit额外信息来指示。

```
# 代码可直接运行
python deducePK.py
```

## API

```python
# 生成测试数据
private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6'\
             '994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
data = b"111"
sm2_crypt = sm2.CryptSM2(public_key=public_key, private_key=private_key)
R_S = sm2_crypt.sign(data, func.random_hex(sm2_crypt.para_len))
print("public key:\n", public_key.lower())
# -------------------------------------------
# [API调用]
R, S = int(R_S[:64], 16), int(R_S[64:], 16)
getPK(R, S, data, sm2_crypt)
```

## Demo

![image-20220730123251438](https://raw.githubusercontent.com/lazypip/readme_pices/main/crypto_pic/image-20220730123251438.png)

