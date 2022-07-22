#pragma once
#ifndef CPPSM4
#define CPPSM4

#define SM4_GROUP_LEN 16
#define SM4_BLOCK_LEN 4
#define SM4_BLOCK_NUM 8

#define SM4_RK_NUM 32
#define SM4_RK_LEN 4

#define SM4_ROUND 32

typedef uint32_t block;
typedef uint8_t byte;

// utility function
void block_hex(block* msg);  // 输出1 block表示的值
void block_str(block* msg);  // 输出1 block在内存中的表示
void demo_plt(block* plt_demo);  // 明文示例

class cppSM4 {
private:
	block* textIn_ptr;  // 输入
	block* textOut_ptr;  // 输出指针 memcpy

	block* key;  // 初始密钥 4 block
	block* rk;  // 轮密钥    32 block
	block* res;  // 存储中间计算值

public:
	cppSM4(byte* text, byte* textOut, byte* key);
	~cppSM4();

	void init();
	void encrypt();
	void decrypt();

	// 计算函数
	void generateKey();  // 生成轮密钥
	block F(block& cur_rk);  // 论函数
	block T(block& input, bool mode);  // 合成置换
	byte sbox(byte& input);
	block lshift(block& input, int size);  // 循环左移
};


#endif // !CPPSM4
