# Speeding up SM4 in C++

## Description

使用以下方式对SM4进行优化：

1. 循环展开, 减少重复计算
2. prebuild T - table
3. AVX SIMD 

以加密$10^6$个Block进行测试，以时钟(clock_t)为单位计算时间。

```
// 代码可直接运行, 建议使用visual studio
g++ -o speedup.out main.cpp cppSM4.cpp
```

## Comparison

​	根据如下测试数据，此项目代码将SM4的加密速度提升 2 倍、

|     Naive     | loop unrolling |    T-table    | T-table + SIMD |
| :-----------: | :------------: | :-----------: | :------------: |
| 48143 Circles | 47011 Circles  | 29921 Circles | 24096 Circles  |

## Demo

![image-20220730174819301](https://raw.githubusercontent.com/lazypip/readme_pices/main/crypto_pic/image-20220730174819301.png)