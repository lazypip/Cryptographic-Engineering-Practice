from TpDec import TpDec


def main():
    d1, d2 = TpDec.generateDK()
    pk = TpDec.generatePK(d1, d2)
    
    print(d1, d2, pk)

    msg = 'Hello World'
    msg = bytes.hex(msg.encode(encoding='utf-8'))

    C = TpDec.encrypt(msg, pk)

    res = TpDec.decrypt(d1, C, d2)
    res = (bytes.fromhex(res)).decode(encoding='utf-8')
    print("Decrypted msg:", res.lstrip('\x00'))


main()
