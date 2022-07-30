#include <iostream>
#include <iomanip>
#include <time.h>
#include "SM3.h"
using namespace std;

int main() {
	char msg[] = "abc";

	cout << "msg: " << msg << endl;
	cout << "Hash: " << endl;


	clock_t s_time = clock();
	SM3 hash = SM3(msg, sizeof(msg) - 1);
	hash.init();
	hash.getHash();

	cout << "Circles used:" << endl <<
		clock() - s_time << " Circles per block" << endl;  // Ê±ÖÓµ¥Ôª
	return 0;
}