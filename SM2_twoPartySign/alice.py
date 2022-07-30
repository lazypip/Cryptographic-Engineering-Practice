from TpSign import TpSign, hex_t
from gmssl import sm2
from gmssl.sm3 import sm3_hash, bytes_to_list

if __name__ == "__main__":
    msg = b'Hello World'
    d1: int = 29961548851145005752492999631966189269019961579632395037624588624422867869608

    P: hex_t = TpSign.aliceR1(d1)  # 公钥64 bytes
    k1 = TpSign.aliceR2(msg)
    sign: hex_t = TpSign.aliceR3(d1, k1)
    print("Msg: ", msg)
    print("Get Signature:", sign)

    # Verify the sig
    sm2_crypt = sm2.CryptSM2(public_key=P, private_key='00')
    msg_hash: hex_t = sm3_hash(bytes_to_list(msg))
    msg_hash: bytes = bytes.fromhex(msg_hash)

    if sm2_crypt.verify(sign, msg_hash):
        print("Valid Signature")
    else:
        print("Wrong Signature")
