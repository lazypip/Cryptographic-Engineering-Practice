#include <algorithm>
#include <iostream>
#include <stdint.h>
#include <cassert>
#include <stdlib.h>

#include <immintrin.h>  // avx-256 bit

#include "cppSM4.h"
using namespace std;



const byte sBox_data[0x10][0x10] = {
	 {0xd6, 0x90, 0xe9, 0xfe, 0xcc, 0xe1, 0x3d, 0xb7, 0x16, 0xb6, 0x14, 0xc2, 0x28, 0xfb, 0x2c, 0x05},
	 {0x2b, 0x67, 0x9a, 0x76, 0x2a, 0xbe, 0x04, 0xc3, 0xaa, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99},
	 {0x9c, 0x42, 0x50, 0xf4, 0x91, 0xef, 0x98, 0x7a, 0x33, 0x54, 0x0b, 0x43, 0xed, 0xcf, 0xac, 0x62},
	 {0xe4, 0xb3, 0x1c, 0xa9, 0xc9, 0x08, 0xe8, 0x95, 0x80, 0xdf, 0x94, 0xfa, 0x75, 0x8f, 0x3f, 0xa6},
	 {0x47, 0x07, 0xa7, 0xfc, 0xf3, 0x73, 0x17, 0xba, 0x83, 0x59, 0x3c, 0x19, 0xe6, 0x85, 0x4f, 0xa8},
	 {0x68, 0x6b, 0x81, 0xb2, 0x71, 0x64, 0xda, 0x8b, 0xf8, 0xeb, 0x0f, 0x4b, 0x70, 0x56, 0x9d, 0x35},
	 {0x1e, 0x24, 0x0e, 0x5e, 0x63, 0x58, 0xd1, 0xa2, 0x25, 0x22, 0x7c, 0x3b, 0x01, 0x21, 0x78, 0x87},
	 {0xd4, 0x00, 0x46, 0x57, 0x9f, 0xd3, 0x27, 0x52, 0x4c, 0x36, 0x02, 0xe7, 0xa0, 0xc4, 0xc8, 0x9e},
	 {0xea, 0xbf, 0x8a, 0xd2, 0x40, 0xc7, 0x38, 0xb5, 0xa3, 0xf7, 0xf2, 0xce, 0xf9, 0x61, 0x15, 0xa1},
	 {0xe0, 0xae, 0x5d, 0xa4, 0x9b, 0x34, 0x1a, 0x55, 0xad, 0x93, 0x32, 0x30, 0xf5, 0x8c, 0xb1, 0xe3},
	 {0x1d, 0xf6, 0xe2, 0x2e, 0x82, 0x66, 0xca, 0x60, 0xc0, 0x29, 0x23, 0xab, 0x0d, 0x53, 0x4e, 0x6f},
	 {0xd5, 0xdb, 0x37, 0x45, 0xde, 0xfd, 0x8e, 0x2f, 0x03, 0xff, 0x6a, 0x72, 0x6d, 0x6c, 0x5b, 0x51},
	 {0x8d, 0x1b, 0xaf, 0x92, 0xbb, 0xdd, 0xbc, 0x7f, 0x11, 0xd9, 0x5c, 0x41, 0x1f, 0x10, 0x5a, 0xd8},
	 {0x0a, 0xc1, 0x31, 0x88, 0xa5, 0xcd, 0x7b, 0xbd, 0x2d, 0x74, 0xd0, 0x12, 0xb8, 0xe5, 0xb4, 0xb0},
	 {0x89, 0x69, 0x97, 0x4a, 0x0c, 0x96, 0x77, 0x7e, 0x65, 0xb9, 0xf1, 0x09, 0xc5, 0x6e, 0xc6, 0x84},
	 {0x18, 0xf0, 0x7d, 0xec, 0x3a, 0xdc, 0x4d, 0x20, 0x79, 0xee, 0x5f, 0x3e, 0xd7, 0xcb, 0x39, 0x48} };

const block FK[4] = { 0xA3B1BAC6, 0x56AA3350, 0x677D9197, 0xB27022DC };

const block CK[32] = {
	 0x00070e15, 0x1c232a31, 0x383f464d, 0x545b6269,
	 0x70777e85, 0x8c939aa1, 0xa8afb6bd, 0xc4cbd2d9,
	 0xe0e7eef5, 0xfc030a11, 0x181f262d, 0x343b4249,
	 0x50575e65, 0x6c737a81, 0x888f969d, 0xa4abb2b9,
	 0xc0c7ced5, 0xdce3eaf1, 0xf8ff060d, 0x141b2229,
	 0x30373e45, 0x4c535a61, 0x686f767d, 0x848b9299,
	 0xa0a7aeb5, 0xbcc3cad1, 0xd8dfe6ed, 0xf4fb0209,
	 0x10171e25, 0x2c333a41, 0x484f565d, 0x646b7279 };


cppSM4::cppSM4(byte* text, byte* key_in) {
	/// <summary>
	/// 读入plaintext, key指针
	/// result, rk指针置空
	/// </summary>
	/// <param name="text"></param>
	/// <param name="textOut"></param>
	/// <param name="key_in"></param>
	textIn_ptr = (block*)text;
	key = (block*)key_in;

	res = nullptr;
	rk = nullptr;

	T_ptr = nullptr;
}


cppSM4::~cppSM4() {
	/// <summary>
	/// 销毁res, rk
	/// </summary>
	if (res != nullptr) {
		delete[] res;
	}
	if (rk != nullptr) {
		delete[] rk;
	}
	if (T_ptr != nullptr) {
		for (int i = 0; i < 4; i++)
			delete[] T_ptr[i];
		delete[] T_ptr;
	}
}


void cppSM4::init() {
	/// <summary>
	/// res -> X0, X1, X2, X3
	/// rk ->  k0, k1, ..., k31
	/// </summary>
	res = new block[4];  // 16 bytes
	for (int i = 0; i < SM4_BLOCK_LEN; i++) {
		res[i] = textIn_ptr[i];
		// 转化为大端存储
		res[i] = _byteswap_ulong(res[i]);
	}

	// 生成32个4 byte轮密钥
	rk = new block[SM4_RK_NUM];
	generateKey();
}


void cppSM4::encrypt(byte* textOut_ptr) {
	// [32次迭代变化]
	block new_block = 0x00;

	for (int round = 0; round < SM4_ROUND; round++) {
		new_block = F(rk[round]);  // 生成下一 Xi

		// 更新res
		res[0] = res[1], res[1] = res[2];
		res[2] = res[3], res[3] = new_block;
	}

	// [转回小端 + 反序变换]
	for (int i = 0; i < 4; i++)
		res[i] = _byteswap_ulong(res[i]);
	swap(res[0], res[3]), swap(res[1], res[2]);

	// [输出至textOut_ptr]
	if (textOut_ptr == nullptr) {
		fprintf(stderr, "no enough mem \n");
		exit(1);
	}
	memcpy_s(textOut_ptr, SM4_GROUP_LEN, res, SM4_GROUP_LEN);
}

void cppSM4::decrypt(byte* textOut_ptr) {
	// 反序轮密钥
	int i = 0, j = SM4_RK_NUM - 1;
	while (i <= j) {
		swap(rk[i], rk[j]);
		i++, j--;
	}
	encrypt(textOut_ptr);
}


void cppSM4::generateKey() {
	/// <summary>
	/// rk ->  k0, k1, ..., k31
	/// </summary>

	// 生成 K0 K1 K2 K3
	block* rk_queue = new block[4];
	memcpy_s(rk_queue, 16, key, 16);
	for (int i = 0; i < 4; i++) {
		rk_queue[i] = _byteswap_ulong(rk_queue[i]);  // 改为大端存储
		rk_queue[i] ^= FK[i];
	}
	// 生成轮密钥
	for (int i = 0; i < SM4_ROUND; i++) {
		block T_input = rk_queue[1] ^ rk_queue[2] ^ rk_queue[3] ^ CK[i];
		block new_rk = rk_queue[0] ^ T(T_input, true);
		rk_queue[0] = rk_queue[1], rk_queue[1] = rk_queue[2];
		rk_queue[2] = rk_queue[3], rk_queue[3] = new_rk;
		rk[i] = new_rk;
	}

	delete[] rk_queue;
}


block cppSM4::F(block& cur_rk) {
	block input_T = res[1] ^ res[2] ^ res[3] ^ cur_rk;
	block res_T = 0x00;

	if (T_ptr == nullptr) {
		res_T = T(input_T, false);
	}
	else {  // 优化
		res_T = T_opt(input_T);
	}
	return res[0] ^ res_T;
}


block cppSM4::T(block& input, bool mode_key = false) {
	// 置换转为字节串
	input = _byteswap_ulong(input);
	// 以byte为单位处理
	byte* data = (byte*)&input;
	byte res_1[4] = { 0x00 };

	// 非线性变换
	for (int i = 0; i < SM4_BLOCK_LEN; i++)
		res_1[i] = sbox(data[i]);
	input = _byteswap_ulong(input);  // 字节串转回

	block* res_2 = (block*)res_1;  
	*res_2 = _byteswap_ulong(*res_2);// 字节串转回
	// 密钥生成线性变换
	if (mode_key) {
		block res = *res_2 ^ lshift(*res_2, 13) ^ lshift(*res_2, 23);
		return res;
	}

	// 加密线性变化
	block res_3 = *res_2 ^ lshift(*res_2, 2) ^ lshift(*res_2, 10);
	res_3 ^= lshift(*res_2, 18) ^ lshift(*res_2, 24);
	return res_3;
}


byte cppSM4::sbox(byte& input) {
	byte row = input >> 4;  // 前4 bit决定行
	byte col = input % 0x10;  // 后4 bit决定列
	return sBox_data[row][col];
}


block cppSM4::lshift(block& input, int size) {
	block l = input << size, r = input >> (32 - size);
	return l | r;
}


// ---------------- optimization function -----------
void cppSM4::Ttable_build() {
	// 分配空间
	T_ptr = new block* [4];
	for (int i = 0; i < 4; i++)
		T_ptr[i] = new block[0xff];

	// 计算, 其他字节置sbox(0x00)
	int size[4] = { 24, 16, 8, 0 };
	for (int i = 0; i < 4; i++) {
		for (byte x = 0; x < 0xff; x++) {
			block tmp = sbox(x);
			tmp = lshift(tmp, size[i]);
			// tmp = _byteswap_ulong(tmp);  // 字节串转回

			block res = tmp ^ lshift(tmp, 2) ^ lshift(tmp, 10);
			res ^= lshift(tmp, 18) ^ lshift(tmp, 24);
			T_ptr[i][x] = res;
		}
	}
}

block cppSM4::Ttable(byte in, int box_num) {
	if (T_ptr == nullptr)
		Ttable_build();
	
	return T_ptr[box_num][in];
}


block cppSM4::T_opt(block& input) {
	if (T_ptr == nullptr)
		Ttable_build();

	// 转为字节串
	input = _byteswap_ulong(input);
	// 以byte为单位处理
	byte* data = (byte*)&input;

	block Sbox_0 = Ttable(data[0], 0);
	block Sbox_1 = Ttable(data[1], 1);
	block Sbox_2 = Ttable(data[2], 2);
	block Sbox_3 = Ttable(data[3], 3);

	// 转回
	input = _byteswap_ulong(input);
	return Sbox_0 ^ Sbox_1 ^ Sbox_2 ^ Sbox_3;
}


// ---------------- utility function ----------------
void block_hex(block* msg) {  // 不使用
	byte* tmp_ptr = (byte*)msg;
	fprintf(stdout, "Value of a block: \n0x");

	for (int i = SM4_BLOCK_LEN - 1; i >= 0; i--) {
		fprintf(stdout, "%02X ", tmp_ptr[i]);
	}
	fprintf(stdout, "\n");
}


void block_str(block* msg)
{
	byte* tmp_ptr = (byte*)msg;
	fprintf(stdout, "block in mem: \n");

	for (int i = 0; i <= SM4_BLOCK_LEN - 1; i++) {
		fprintf(stdout, "%02X ", tmp_ptr[i]);
	}
	fprintf(stdout, "\n");
}

void demo_plt(block* plt_demo)
{
	if (plt_demo == nullptr) {
		fprintf(stderr, "invalid pointer\n");
		exit(1);
	}
	// 解释为字符
	plt_demo[0] = 0x67452301;
	plt_demo[1] = 0xEFCDAB89;
	plt_demo[2] = 0x98BADCFE;
	plt_demo[3] = 0x10325476;
}


void Qblock_str(block* msg) {
	byte* tmp_ptr = (byte*)msg;

	for (int i = 0; i <= SM4_BLOCK_LEN * 4 - 1; i++) {
		fprintf(stdout, "%02X", tmp_ptr[i]);
	}
	fprintf(stdout, "\n");
}
