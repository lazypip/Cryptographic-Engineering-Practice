default_ecc_table = {
    'n': 'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123',
    'p': 'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF',
    'g': '32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7'\
         'bc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0',
    'a': 'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC',
    'b': '28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93',
}

def legendre_symbol(a, p):
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls

def modular_sqrt(a, p):
    # Simple cases
    #
    if legendre_symbol(a, p) != 1:
        return 0
    elif a == 0:
        return 0
    elif p == 2:
        return p
    elif p % 4 == 3:
        return pow(a, (p + 1) // 4, p)

    # Partition p-1 to s * 2^e for an odd s (i.e.
    # reduce all the powers of 2 from p-1)
    #
    s = p - 1
    e = 0
    while s % 2 == 0:
        s //= 2
        e += 1

    # Find some 'n' with a legendre symbol n|p = -1.
    # Shouldn't take long.
    #
    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1
    x = pow(a, (s + 1) // 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e

    while True:
        t = b
        m = 0
        for m in range(r):
            if t == 1:
                break
            t = pow(t, 2, p)

        if m == 0:
            return x

        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m


def neg_point(P1):
    """ hex -> hex
    -(x, y) = (x, p - y) , 32 bytes + 32 bytes"""
    p = int(default_ecc_table['p'], 16)  # 32 bytes
    x = P1[:64]  # 32 bytes
    y = int(P1[64:], 16)
    y = hex(p - y)[2:]

    return x + y


def ex_euc(j, k):
    if j == k:
        return (j, 1, 0)
    else:
        i = 0
        j_array = [j]
        k_array = [k]
        q_array = []
        r_array = []

        prev_r_is_zero = False

        while not (prev_r_is_zero):
            q_array.append(k_array[i]//j_array[i])
            r_array.append(k_array[i]%j_array[i])
            k_array.append(j_array[i])
            j_array.append(r_array[i])
            i += 1
            if r_array[i-1] == 0:
                prev_r_is_zero = True
        i -= 1
        gcd = j_array[i]
        x_array = [1]
        y_array = [0]

        i -= 1
        total_steps = i

        while i >= 0:
            y_array.append(x_array[total_steps-i])
            x_array.append(y_array[total_steps-i] - q_array[i]*x_array[total_steps-i])
            i -= 1

        return (gcd, x_array[-1], y_array[-1])


def mod_inverse(j, n):
    (gcd, x, y) = ex_euc(j, n)

    if gcd == 1:
        return x%n
    else:
        return -1


def ecc_add(p: str, q: str) -> str:
    """
    para : hex, ret : hex
    """
    p = [int(p[:64], 16), int(p[64:], 16)]
    q = [int(q[:64], 16), int(q[64:], 16)]

    if p[0] > q[0]:
        temp = p
        p = q
        q = temp
    r = []
    P = int(default_ecc_table['p'], 16)
    slope = (q[1] - p[1])*mod_inverse(q[0] - p[0], P) % P

    r.append((slope**2 - p[0] - q[0]) % P)
    r.append((slope*(p[0] - r[0]) - p[1]) % P)

    return hex(r[0])[2:].rjust(64, '0') + hex(r[1])[2:].rjust(64, '0')
