#include <iostream>
#include <iomanip>
#include "SM3.h"
using namespace std;

int main() {
	char msg[4] = "abc";
	size_t msg_len = sizeof(msg) - 1;
	SM3 hash = SM3(msg, msg_len);
	hash.getHash();

	return 0;
}