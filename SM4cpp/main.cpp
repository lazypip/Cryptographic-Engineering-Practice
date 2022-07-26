#include <iostream>
#include "cppSM4.h"
using namespace std;

int main() {
	block plaintxt[4] = { 0x00 };
	block key[4] = { 0x00 };
	demo_plt(plaintxt);
	demo_plt(key);

	block ciphertxt[4] = { 0x00 };
	cppSM4 enc = cppSM4((byte*)plaintxt, (byte*)ciphertxt, (byte*)key);
	enc.init();
	enc.encrypt();

	printf("\nciphertxt\n");
	for (int i = 0; i < 4; i++)
		block_str(&ciphertxt[i]);

	// --------------------------------------
	cout << endl;
	cppSM4 dec = cppSM4((byte*)ciphertxt, (byte*)plaintxt, (byte*)key);
	dec.init();
	dec.decrypt();

	printf("\nplaintxt\n");
	for (int i = 0; i < 4; i++)
		block_str(&plaintxt[i]);

	return 0;
}