# length extension attack for SM3

## Description

​	由于SM3使用MD结构，因此可以根据填充好的消息M1及hash(M1)，计算出$hash(M1|M2)$，其中M2为任意消息。具体方法为将hash(M1)作为压缩函数的输入。

```
# 代码可直接运行
python SM3_lenExtend.py
```



## API

```python
# 原始消息
prehash: SM3 = SM3("abcd")
prehash = prehash.getResult(hexdig=False)

extend_msg = "efgh"
# [扩展API]
SM3_extend(extend_msg, prehash)
```

## Demo

![image-20220730165136481](https://raw.githubusercontent.com/lazypip/readme_pices/main/crypto_pic/image-20220730165136481.png)