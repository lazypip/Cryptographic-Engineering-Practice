# birthday attack of reduced SM3

## Description

​	对**32bit**的简化SM3生日攻击，寻找碰撞。根据生日攻击，需要的时间复杂度为$O(2^{16})$。具体方法为随机生成两个表，每个表包含$2^{16}$个字符串及其哈希值。判断表A的每一个元素的哈希值是否在B中出现。

```
# 代码可直接运行
python birthattack.py
```

## API

```
generateHash()  # 生成随机字符及hash
birthAttack()  # 自动寻找碰撞
```

## Result

找到以下碰撞结果（32bit）

|   msg1    | hash(msg2)=hash(msg1) |
| :-------: | :-------------------: |
| j#}&{68X  |       3;7$^ATu        |
| 85qN#8'S  |       <?)^bqNA        |
| +tlW,\E"  |       P. JAbz"        |
| 5V"\n'tC6 |       X@mH*<5;        |
| Cfv~?]Ru  |       4[SOZc;7        |

## Demo

![image-20220730162108334](https://raw.githubusercontent.com/lazypip/readme_pices/main/crypto_pic/image-20220730162108334.png)