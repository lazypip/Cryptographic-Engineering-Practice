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
void block_hex(block* msg);  // ���1 block��ʾ��ֵ
void block_str(block* msg);  // ���1 block���ڴ��еı�ʾ
void demo_plt(block* plt_demo);  // ����ʾ��

class cppSM4 {
private:
	block* textIn_ptr;  // ����
	block* textOut_ptr;  // ���ָ�� memcpy

	block* key;  // ��ʼ��Կ 4 block
	block* rk;  // ����Կ    32 block
	block* res;  // �洢�м����ֵ

public:
	cppSM4(byte* text, byte* textOut, byte* key);
	~cppSM4();

	void init();
	void encrypt();
	void decrypt();

	// ���㺯��
	void generateKey();  // ��������Կ
	block F(block& cur_rk);  // �ۺ���
	block T(block& input, bool mode);  // �ϳ��û�
	byte sbox(byte& input);
	block lshift(block& input, int size);  // ѭ������
};


#endif // !CPPSM4
