#include <stdint.h>
#include <iostream>
#include <cmath>
#include <stdlib.h>
#include "SM3.h"

using namespace std;

block IV[HASH_LEN / BLOCK_LEN] = {
	0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600,
	0xa96f30bc, 0x163138aa, 0xe38dee4d, 0xb0fb0e4e };

SM3::SM3(char* msg_in, size_t msg_len_in) {
	msg = msg_in;
	msg_ptr = (block*)msg;
	input_pre = nullptr;

	msg_len = msg_len_in;
	msg_mod_len = msg_len % GROUP_LEN;
	
	init();
}

SM3::~SM3() {
	if (input_pre != nullptr)
		delete[] input_pre;
	input_pre = nullptr;
	msg = nullptr;
}

void SM3::init() {
	// IV赋值
	input_pre = new block[HASH_LEN / BLOCK_LEN];
	memcpy_s(input_pre, HASH_LEN, IV, HASH_LEN);
}


void SM3::update() {
	/*W - 68*/
	block W[68] = { 0x00 };
	memcpy_s(W, GROUP_LEN, msg_ptr, GROUP_LEN);

	// 异或运算时转为整形
	for (int i = 0; i <= 15; i++) {
		W[i] = _byteswap_ulong(W[i]);
	}

	for (int j = 16; j <= 67; j++) {
		W[j] = W[j - 6] ^ lshift(W[j - 13], 7);
		block tmp = W[j - 16] ^ W[j - 9] ^ lshift(W[j - 3], 15);
		W[j] = W[j] ^ P1(tmp);
	}

	/* WW - 64 */
	block WW[64] = { 0x00 };
	for (int j = 0; j < 64; j++)
		WW[j] = W[j] ^ W[j + 4];

	///* 转回字节串 */
	//for (int i = 0; i < 68; i++) {
	//	W[i] = _byteswap_ulong(W[i]);
	//}
	//for (int i = 0; i < 64; i++) {
	//	WW[i] = _byteswap_ulong(WW[i]);
	//}

	/* 压缩函数 */
	block A = input_pre[0], B = input_pre[1], C = input_pre[2], D = input_pre[3];
	block E = input_pre[4], F = input_pre[5], G = input_pre[6], H = input_pre[7];
	block SS1, SS2, TT1, TT2;
	for (int j = 0; j < 64; j++) {
		block tmp = T(j);
		SS1 = lshift(A, 12) + E + lshift(tmp, j);
		SS1 = lshift(SS1, 7);

		SS2 = SS1 ^ lshift(A, 12);

		TT1 = FF(A, B, C, j) + D + SS2 + WW[j];
		TT2 = GG(E, F, G, j) + H + SS1 + W[j];

		D = C;
		C = lshift(B, 9);
		B = A;
		A = TT1;
		H = G;
		G = lshift(F, 19);
		F = E;
		E = P0(TT2);
	}
	input_pre[0] ^= A, input_pre[1] ^= B, input_pre[2] ^= C, input_pre[3] ^= D;
	input_pre[4] ^= E, input_pre[5] ^= F, input_pre[6] ^= G, input_pre[7] ^= H;

	for (int i = 0; i < 8; i++) {
		input_pre[i] = _byteswap_ulong(input_pre[i]);
	}
}


void SM3::final() {
	/* 进行填充 */
	// 需要2个GROUP
	if (msg_mod_len + 1 + 8 > GROUP_LEN) {
		char* msg_end = new char[2 * GROUP_LEN];
		memset(msg_end, 0x00, 2 * GROUP_LEN);
		memcpy_s(msg_end, msg_mod_len, msg_ptr, msg_mod_len);

		msg_end[msg_mod_len] = (uint8_t)0x80;  // 填充 1 byte
		uint64_t msg_len_padding = _byteswap_uint64(msg_len * 8);  // 内存中转为大端
		memcpy_s(msg_end + 2 * GROUP_LEN - 8, 0x08, &msg_len_padding, 0x08);

		msg_ptr = (block*)msg_end;
		update();
		msg_ptr += GROUP_LEN / BLOCK_LEN;
		update();
		delete[] msg_end;
		return;
	}

	// 只需要1个GROUP
	char* msg_end = new char[GROUP_LEN];
	memset(msg_end, 0x00, GROUP_LEN);
	memcpy_s(msg_end, msg_mod_len, msg_ptr, msg_mod_len);

	msg_end[msg_mod_len] = (uint8_t)0x80;  // 填充 1 byte
	uint64_t msg_len_padding = _byteswap_uint64(msg_len * 8);  // 内存中转为大端
	memcpy_s(msg_end + GROUP_LEN - 8, 0x08, &msg_len_padding, 0x08);  // 填充长度

	msg_ptr = (block*)msg_end;
	update();
	delete[] msg_end;
}


void SM3::getHash() {
	// 普通block，即已处理的字节数小于待处理的字节数
	while ((char*)msg_ptr - msg < msg_len - msg_mod_len) {
		update();
		msg_ptr = msg_ptr + GROUP_LEN / BLOCK_LEN;  // 指向下一block
	}
	final();
	uint8_t* output = (uint8_t*)input_pre;
	for (int i = 0; i < HASH_LEN; i++)
		printf("%02X ", (int)output[i]);  // 进行填充
	printf("\n");
}


// ------------------------ 中间计算函数 -------------------------
block SM3::T(size_t j) {
	/* 返回 block 32bit 数据 */
	if (j < 16) return 0x79cc4519;
	else return 0x7a879d8a;
}

block SM3::FF(block x, block y, block z, size_t j) {
	if (j < 16)
		return x ^ y ^ z;
	return (x & y) | (x & z) | (y & z);
}

block SM3::GG(block x, block y, block z, size_t j) {
	if (j < 16)
		return x ^ y ^ z;
	return (x & y) | (~x & z);
}

block SM3::lshift(block& x, size_t len) {
	block l = x << len, r = x >> (32 - len);
	return l | r;
}

block SM3::P0(block& x) {
	return x ^ lshift(x, 9) ^ lshift(x, 17);
}

block SM3::P1(block& x) {
	return x ^ lshift(x, 15) ^ lshift(x, 23);
}
