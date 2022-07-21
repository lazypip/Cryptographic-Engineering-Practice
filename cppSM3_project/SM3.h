#ifndef SM3
#define SM3_CPP

// �����ֽ�Ϊ��λ
#define GROUP_LEN 64
#define HASH_LEN 32

// ��С���㵥Ԫ uint32_t 4�ֽ�
#define BLOCK_LEN 4
typedef uint32_t block;

class SM3 {
private:
	char* msg;
	block* msg_ptr;  // ָ����һGROUP
	block* input_pre;   // INPUT_LEN 32 byte

	uint64_t msg_len;  // msg �ֽڳ���
	size_t msg_mod_len;  // ��Ҫ���Ĳ��ֳ���

public:
	SM3(char* msg, size_t msg_len);
	~SM3();

	void init();
	void update();
	void final();
	void getHash();

	// �м���㺯��
	block T(size_t j);
	block FF(block x, block y, block z, size_t j);  // �ɴ�ָ��Ľ�
	block GG(block x, block y, block z, size_t j);

	block lshift(block& x, size_t len);  // ѭ������
	block P0(block& x);
	block P1(block& x);
};

#endif // !SM3


/*

	for (int i = 0; i < GROUP_LEN; i++) {
		uint8_t test = msg_end[i];
		printf("%02X ", test);  // �������
	}
	cout << endl;
	exit(0);

*/