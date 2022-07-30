# Implement and optimize SM3 in C++

## Description

​	SM3的C++实现，并使用循环展开、减少重复运算等简单优化方式对1 block的计算做优化。

```
# 代码编译后可直接运行
g++ -o sm3.out main.cpp SM3.cpp
# 推荐使用visual studio运行
```

## API

```c++
#include "SM3.h"
char msg[] = "abc";
SM3 hash = SM3(msg, sizeof(msg) - 1);
hash.init();
hash.getHash();
```

## Result

![image-20220730171142810](https://raw.githubusercontent.com/lazypip/readme_pices/main/crypto_pic/image-20220730171142810.png)

