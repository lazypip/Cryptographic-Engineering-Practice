# Cryptographic-Engineering-Practice

Contents:

- [About Author](https://github.com/lazypip/Cryptographic-Engineering-Practice#about-author)
- [List of Completed Projects](https://github.com/lazypip/Cryptographic-Engineering-Practice#list-of-completed-projects)
- [Questions Left](https://github.com/lazypip/Cryptographic-Engineering-Practice#questions-left)
- [List of Unfinished Projects](https://github.com/lazypip/Cryptographic-Engineering-Practice#list-of-unfinished-projects)

## About Author

完成人：武彦博， GitHub：[lazypip](https://github.com/lazypip)

班级：网安19级2班， 学号：201900460033

说明：

- 所有项目**均本人独自完成**，未组队
- 每个项目有**单独README**进行说明

## List of Completed Projects

### -SM2

- [Deduce public key from signature](https://github.com/lazypip/Cryptographic-Engineering-Practice/tree/main/SM2_deducePK).
- [Verify the sm2 pitfalls with poc code](https://github.com/lazypip/Cryptographic-Engineering-Practice/tree/main/SM2_pitfall).
- [Implement a PGP scheme with sm2](https://github.com/lazypip/Cryptographic-Engineering-Practice/tree/main/SM2_pgp).
- [Implement sm2 2P sign with real network communication](https://github.com/lazypip/Cryptographic-Engineering-Practice/tree/main/SM2_twoPartySign).
- [Implement sm2 2P decrypt with real network communication](https://github.com/lazypip/Cryptographic-Engineering-Practice/tree/main/SM2_twoPartySign).
- [Implement of Google password check scheme](https://github.com/lazypip/Cryptographic-Engineering-Practice/tree/main/SM2_twoPartySign).

### -SM3

- [Implement the birthday attack of reduced SM3](https://github.com/lazypip/Cryptographic-Engineering-Practice/tree/main/SM3_birthAttack).
- [Implement the Rho method of reduced SM3](https://github.com/lazypip/Cryptographic-Engineering-Practice/tree/main/SM3_rhoAttack).
- [Implement length extension attack for SM3](https://github.com/lazypip/Cryptographic-Engineering-Practice/tree/main/SM3_extendAttack).
- [Implement and optimize SM3 in C++](https://github.com/lazypip/Cryptographic-Engineering-Practice/tree/main/SM3cpp).
- [Implement SM3 in python](https://github.com/lazypip/Cryptographic-Engineering-Practice/tree/main/SM3py).

### -SM4

- [Implement SM4 in C++](https://github.com/lazypip/Cryptographic-Engineering-Practice/tree/main/SM4cpp).
- [Speeding up SM4 in C++](https://github.com/lazypip/Cryptographic-Engineering-Practice/tree/main/SM4cpp_optimation).
  - SIMD, T-table, loop unrolling...

### -Bitcoin

- [Forge signature when the signed message is not checked](https://github.com/lazypip/Cryptographic-Engineering-Practice/tree/main/Bitcoin_ecdshForge).

### -Cryptanalysis

以下密码分析项目非布置的项目

- [Impossible differential cryptanalysis](https://github.com/lazypip/Cryptographic-Engineering-Practice/tree/main/break_vigen%C3%A8re).
- [Break vigenère encryption](https://github.com/lazypip/Cryptographic-Engineering-Practice/tree/main/break_vigen%C3%A8re).

## Questions Left

1. 是否有一种方法，来避免频繁的SM3/4大小端转换.
2. SIMD优化SM4时，减少 load / store 的开销(次数).

##  List of Unfinished Projects

- Implement the ECMH scheme.
- Implement Merkle Tree following RFC6962.
- Send a tx on Bitcoin testnet.
- Research report on MPT.
- Write a circuit to prove your CET6 grades.
