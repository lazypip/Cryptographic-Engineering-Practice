# Forge ECDSH Signature

## Description

​	在ECDSH验签时，若仅对签名值进行验证，不验证$e$与$hash(msg)$是否相等，则根据以下推导式可计算出$e', (r',s')$通过验签。

1. $R'=(x',y')=uG+vP$
2. $e'=r'uv^{-1} \ mod \ n$
3. $s'=r'v^{-1} \ mod \ n$

```
# 代码可直接运行
python forge.py
```

## API

```python
# 测试数据
rk = 'B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
pk = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A8308'\
     '1A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'

# 正常签名通过验证
msg = b'Hello World'
sign = ecdshSign(msg, rk)
ecdshVerify(msg, pk, sign)

# [forge API]
e, sign = forge(pk)  # 伪造的消息及签名
print("forged sign", sign)
ecdshVerify(msg, pk, sign, e)
```

## Demo

![image-20220730145600991](https://raw.githubusercontent.com/lazypip/readme_pices/main/crypto_pic/image-20220730145600991.png)

