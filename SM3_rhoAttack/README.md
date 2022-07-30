# Rho method of reduced SM3

## Description

​	对**32bit**的简化SM3寻找如下环形碰撞：
$$
hash(m_1)->hash(m_2)->.....hash(m_i).....->hash(m_j)=hash(m_i)
$$

```
# 代码可直接运行
python rhoAttack.py
```

## API

```python
# index为相遇的索引值
msg, hash, index = rhoAttack()
```

## Demo

在云服务器上的运行结果如下：

![img](https://raw.githubusercontent.com/lazypip/readme_pices/main/crypto_pic/image-speedup.jpg)

