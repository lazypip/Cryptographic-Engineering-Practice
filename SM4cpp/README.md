# Implement SM4 in C++

## Description

​	使用T-table方法C++实现SM4

```
// 代码可直接运行，建议使用visual studio
g++ -o sm4.out main.cpp cppSM4.cpp
```

## API

```c++
#include "cppSM4.h"
// 测试数据
byte plaintxt[] = "\x01\x23\x45\x67\x89\xAB\xCD\xEF\xFE\xDC\xBA\x98\x76\x54\x32\x10";
byte key[] = "\x01\x23\x45\x67\x89\xAB\xCD\xEF\xFE\xDC\xBA\x98\x76\x54\x32\x10";
block enc_buffer[4] = { 0x00 };
block dec_buffer[4] = { 0x00 };
block Qenc_buffer[32] = { 0x00 };

// 加密 API--------------------------------------
cppSM4 enc = cppSM4((byte*)plaintxt, (byte*)key);
enc.init();
block tt = 0xAA567521;
enc.Ttable_build();  // 设置优化方式
enc.encrypt((byte*)enc_buffer);
printf("ciphertxt: ");
Qblock_str(enc_buffer);

// 解密 API--------------------------------------
cppSM4 dec = cppSM4((byte*)enc_buffer, (byte*)key);
dec.init();
dec.Ttable_build();
dec.decrypt((byte*)dec_buffer);
printf("plaintxt:  ");
Qblock_str(dec_buffer);
```

## Demo

![image-20220730173403405](https://raw.githubusercontent.com/lazypip/readme_pices/main/crypto_pic/image-20220730173403405.png)

## Refer

T-table: http://html.rhhz.net/ZGKXYDXXB/20180205.htm