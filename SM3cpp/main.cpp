#include <iostream>
#include <iomanip>
#include "SM3.h"
using namespace std;

int main() {
	char msg[] = "abc";

	SM3 hash = SM3(msg, sizeof(msg) - 1);
	hash.init();
	hash.getHash();

	return 0;
}