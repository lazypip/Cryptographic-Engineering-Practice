from TpDec import TpDec, hex_t

if __name__ == "__main__":
    d2: int = 3558286353967357416362507171307203711966781522372688181489069882296454134884
    pk: hex_t = 'd1416c0d70504c6392260f2b5f1b119bbdc2ccec3935a8069785ddaa2f5725a4173b7135f86'\
                'd06657e64a739c9d06c917d28cdeab8c474ade8c2f72b7377dd7e'

    print("Bob")
    T1 = TpDec._recv(('127.0.0.1', 8888))
    T2 = TpDec.generateT2(d2, T1)
    TpDec._send(T2, ('127.0.0.1', 7777))
