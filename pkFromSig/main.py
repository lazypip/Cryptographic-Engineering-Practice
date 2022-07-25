import sm2_mod as sm2
from gmssl import func

# 32 bytes
private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
# 64 bytes
public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6'\
            '994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'

data = b"111"
sm2_crypt = sm2.CryptSM2(public_key=public_key, private_key=private_key)
R, S = sm2_crypt.sign(data, func.random_hex(sm2_crypt.para_len))

# 恢复公钥
sm2_crypt.getPK(R, S, data)
