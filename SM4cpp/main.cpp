#include <iostream>
#include <time.h>
#include "cppSM4.h"

using namespace std;

int main() {
	byte plaintxt[] = "\x01\x23\x45\x67\x89\xAB\xCD\xEF\xFE\xDC\xBA\x98\x76\x54\x32\x10";
	byte key[] = "\x01\x23\x45\x67\x89\xAB\xCD\xEF\xFE\xDC\xBA\x98\x76\x54\x32\x10";
	block enc_buffer[4] = { 0x00 };
	block dec_buffer[4] = { 0x00 };
	block Qenc_buffer[32] = { 0x00 };
	
	// 加密--------------------------------------
	cppSM4 enc = cppSM4((byte*)plaintxt, (byte*)key);
	enc.init();
	block tt = 0xAA567521;
	// 设置优化方式
	enc.Ttable_build();
	//block r1 = enc.T_opt(tt);
	//cout << hex << r1 << endl;

	//block r2 = enc.T(tt, false);
	//cout << hex << r2 << endl;


	enc.encrypt((byte*)enc_buffer);

	printf("ciphertxt: ");
	Qblock_str(enc_buffer);

	// 解密--------------------------------------
	cppSM4 dec = cppSM4((byte*)enc_buffer, (byte*)key);
	dec.init();
	dec.Ttable_build();
	dec.decrypt((byte*)dec_buffer);

	printf("plaintxt:  ");
	Qblock_str(dec_buffer);

	return 0;
}
