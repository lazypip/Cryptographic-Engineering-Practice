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
	

	// δ�Ż�
	cppSM4 enc = cppSM4((byte*)plaintxt, (byte*)key);
	enc.init();

	clock_t s_time = clock();
	for (int i = 0; i < 10000000; i++) {
		enc.encrypt((byte*)enc_buffer);
	}
	cout << clock() - s_time << " Circles" << endl;  // ʱ�ӵ�Ԫ


	// ��ѭ��չ��
	cppSM4 enc_opt1 = cppSM4((byte*)plaintxt, (byte*)key);
	enc_opt1.init();
	enc_opt1.unrollLoop();

	clock_t s_time_opt1 = clock();
	for (int i = 0; i < 10000000; i++) {
		enc_opt1.encrypt((byte*)enc_buffer);
	}
	cout << clock() - s_time_opt1 << " Circles" << endl;  // ʱ�ӵ�Ԫ


	// ��T table �Ż�
	cppSM4 enc_opt2 = cppSM4((byte*)plaintxt, (byte*)key);
	enc_opt2.init();
	enc_opt2.Ttable_build();  // Ԥ���� T-table

	clock_t s_time_opt2 = clock();
	for (int i = 0; i < 10000000; i++) {
		enc_opt2.encrypt((byte*)enc_buffer);
	}
	cout << clock() - s_time_opt2 << " Circles" << endl;  // ʱ�ӵ�Ԫ


	// SIMD + T table
	byte Qplaintxt[] = 
		"\x01\x23\x45\x67\x89\xAB\xCD\xEF\xFE\xDC\xBA\x98\x76\x54\x32\x10"\
		"\x01\x23\x45\x67\x89\xAB\xCD\xEF\xFE\xDC\xBA\x98\x76\x54\x32\x10"\
		"\x01\x23\x45\x67\x89\xAB\xCD\xEF\xFE\xDC\xBA\x98\x76\x54\x32\x10"\
		"\x01\x23\x45\x67\x89\xAB\xCD\xEF\xFE\xDC\xBA\x98\x76\x54\x32\x10"\
		"\x01\x23\x45\x67\x89\xAB\xCD\xEF\xFE\xDC\xBA\x98\x76\x54\x32\x10"\
		"\x01\x23\x45\x67\x89\xAB\xCD\xEF\xFE\xDC\xBA\x98\x76\x54\x32\x10"\
		"\x01\x23\x45\x67\x89\xAB\xCD\xEF\xFE\xDC\xBA\x98\x76\x54\x32\x10"\
		"\x01\x23\x45\x67\x89\xAB\xCD\xEF\xFE\xDC\xBA\x98\x76\x54\x32\x10";
	
	cppSM4 enc_opt3 = cppSM4((byte*)Qplaintxt, (byte*)key);
	enc_opt3.Qinit_SIMD();
	enc_opt3.Ttable_build();  // Ԥ���� T-table

	clock_t s_time_opt3 = clock();
	for (int i = 0; i < int(10000000 / 8); i++) {
		enc_opt3.Qencrypt_SIMD((byte*)Qenc_buffer);
	}
	cout << clock() - s_time_opt3 << " Circles" << endl;  // ʱ�ӵ�Ԫ


	return 0;
}

/*
	// ����--------------------------------------
	cppSM4 enc = cppSM4((byte*)plaintxt, (byte*)key);
	enc.init();
	// �����Ż���ʽ
	enc.Ttable_build();

	clock_t s_time = clock();
	enc.encrypt((byte*)enc_buffer);

	printf("ciphertxt: ");
	Qblock_str(enc_buffer);

	// ����--------------------------------------
	cppSM4 dec = cppSM4((byte*)enc_buffer, (byte*)key);
	dec.init();
	dec.decrypt((byte*)dec_buffer);

	printf("plaintxt:  ");
	Qblock_str(dec_buffer);

*/
