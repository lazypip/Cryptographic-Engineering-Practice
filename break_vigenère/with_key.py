'''通过明文与密钥实现维吉尼亚加密
   支持大小写
   若有其他字符(包括空字符)则不当作字母字符处理,仅保留'''

from string import ascii_lowercase, ascii_uppercase

def encryption(key, msg,ex=1):
    '''输入密钥字符串与明文字符串 ex为是否保留其他符号，默认保留 =1
     返回密文字符串 '''
    key_len = len(key); key = key.lower()  # 将key转为小写
    target = ""  #密文
    #将密钥转换成位移量
    key_list = []
    for i in key:
        key_list.append(ascii_lowercase.index(i))

    k = 0  # 指示对应密钥字母
    for j in msg:
        if j in ascii_lowercase:
            mod = (ascii_lowercase.index(j) + key_list[k]) % 26
            target += ascii_lowercase[mod]
            k = (k + 1) % key_len
        elif j in ascii_uppercase:
            mod = (ascii_uppercase.index(j) + key_list[k]) % 26
            target += ascii_uppercase[mod]
            k = (k + 1) % key_len
        else:
            if ex==1:
                target += j
    return target


def decryption(key,en_msg,ex=1):
    '''输入密钥字符串与密文字符串 ex为是否保留其他符号，默认保留 =1
    返回明文字符串 '''
    key_len = len(key);
    key = key.lower()  # 将key转为小写
    target = ""  # 密文
    # 将密钥转换成位移量
    key_list = []
    for i in key:
        key_list.append(ascii_lowercase.index(i))

    k = 0  # 指示对应密钥字母
    for j in en_msg:
        if j in ascii_lowercase:
            mod = (ascii_lowercase.index(j) - key_list[k] + 26) % 26
            target += ascii_lowercase[mod]
            k = (k + 1) % key_len
        elif j in ascii_uppercase:
            mod = (ascii_uppercase.index(j) - key_list[k] + 26) % 26
            target += ascii_uppercase[mod]
            k = (k + 1) % key_len
        else:
            if ex==1:
                target += j
    return target

if __name__ == "__main__":
    key = input("输入密钥: ")
    msg = input("输入待加密信息:\n  ")
    en_msg = encryption(key, msg,1)
    print("密文为:\n  ", en_msg, sep = "")   #sep表示连接符
    re_msg = decryption(key, en_msg,1)
    print("加密后返回的明文为:\n  ", re_msg, sep="")