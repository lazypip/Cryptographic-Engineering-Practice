from TpDec import TpDec, hex_t

if __name__ == "__main__":
    d1: int = 10481687648743270113839589774278114049784384775065781287816145589706481668346 
    pk: hex_t = 'd1416c0d70504c6392260f2b5f1b119bbdc2ccec3935a8069785ddaa2f5725a4173b7135f86'\
                'd06657e64a739c9d06c917d28cdeab8c474ade8c2f72b7377dd7e'

    C = [
        '62026868a4ba9293c0f6b7b24b7ce601e03961e4c422840de3f8295e7d866801'\
            '507b2dc69c500afc9d43131d4b91c996f8fe0ca78e60a268d81058c3c0cb95e1', 
        '47343a121e4f5d7d318e78494a74ef8ea143761f0f7ab28833d75e9e6125edd9', 
        '73b75eeb1b47453f8cd4df94dfdac87f9dc26ae310fad56cbe3242f414d560d5'
        ]

    print("Alice")
    res = TpDec.decryptInteract(d1, C, ('127.0.0.1', 7777), ('127.0.0.1', 8888))
    res = (bytes.fromhex(res)).decode(encoding='utf-8')
    print("Decrypted msg:", res.lstrip('\x00'))
