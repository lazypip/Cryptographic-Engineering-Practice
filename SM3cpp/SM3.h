#ifndef SM3
#define SM3_CPP

// 均以字节为单位
#define GROUP_LEN 64
#define HASH_LEN 32

// 最小计算单元 uint32_t 4字节
#define BLOCK_LEN 4
typedef uint32_t block;

class SM3 {
private:
	char* msg;
	block* msg_ptr;  // 指向下一GROUP
	block* input_pre;   // INPUT_LEN 32 byte

	uint64_t msg_len;  // msg 字节长度
	size_t msg_mod_len;  // 需要填充的部分长度

public:
	SM3(char* msg, size_t msg_len);
	~SM3();

	void init();
	void update();
	void final();
	void getHash();

	// 中间计算函数
	block T(size_t j);
	block FF(block x, block y, block z, size_t j);  // 可传指针改进
	block GG(block x, block y, block z, size_t j);

	block lshift(block& x, size_t len);  // 循环左移
	block P0(block& x);
	block P1(block& x);
};

#endif // !SM3


/*

	for (int i = 0; i < GROUP_LEN; i++) {
		uint8_t test = msg_end[i];
		printf("%02X ", test);  // 进行填充
	}
	cout << endl;
	exit(0);

*/