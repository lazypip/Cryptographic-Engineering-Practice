'''破解维吉尼亚密码
   密钥长度函数pre_10
   猜测密钥函数target_key'''
from string import ascii_lowercase

F = [
0.0651738, 0.0124248, 0.0217339,0.0349835, 0.1041442, 0.0197881,
0.0158610, 0.0492888, 0.0558094,0.0009033, 0.0050529, 0.0331490,
0.0202124, 0.0564513, 0.0596302,0.0137645, 0.0008606, 0.0497563,
0.0515760, 0.0729357, 0.0225134,0.0082903, 0.0171272, 0.0013692,
0.0145984, 0.0007836
]
# 英文字符频率 一个明文足够长的平移密码的重合指数接近0.0687

def c_alpha(cipher):   # 去掉非字母后的小写字母密文
    cipher_alpha = ''
    for i in range(len(cipher)):
        if (cipher[i].isalpha()):
            cipher_alpha += cipher[i].lower()
    return cipher_alpha

# 计算cipher的重合指数 即key_len=1时的重合指数(凯撒密码)
def count_CI(cipher):
    N = [0.0 for i in range(26)]  #存储频数
    cipher = c_alpha(cipher)      #变为小写字母
    L = len(cipher)
    # 计算所有字母的频数，存在数组N当中
    for i in cipher:
        N[ascii_lowercase.index(i)] += 1

    #计算密文重合指数
    CI_1 = 0
    for i in range(26):
        CI_1 += (N[i] / L) * ((N[i]-1) / (L-1))  #  *重合指数公式1*
    return CI_1

# 计算秘钥长度为 key_len 的重合指数 分为多个凯撒密码
def count_key_len_CI(cipher,key_len):
    un_cip = ['' for i in range(key_len)]    # un_cip 是分组
    aver_CI = 0.0
    count = 0

    cipher_alpha = c_alpha(cipher)
    for i in range(len(cipher_alpha)):  #将每组的字符组合成字符串
        z = i % key_len
        un_cip[z] += cipher_alpha[i]
    for i in range(key_len):            #计算每组的重合指数
        un_cip[i]= count_CI(un_cip[i])
        aver_CI += un_cip[i]

    aver_CI = aver_CI/len(un_cip)  #每组的平均值
    return aver_CI

# 找出最可能的前十个秘钥长度
def pre_10(cipher):
    M = [(0,0)]+[(1,count_CI(cipher))]+[(0,0.0) for i in range(48)]   #key最大长度为49
    for i in range(1,50):
        M[i] = (i,abs(0.065 - count_key_len_CI(cipher,i)))
    M = sorted(M,key = lambda x:x[1])   #按照数组第二个元素排序
    print("秘钥长度为:")
    for i in range(1,50):  #不包括下标为0的
        print (M[i])

#****************以下为破解密钥过程**************************************************************
# 猜测单个秘钥得到的重合指数 应用到一组凯撒加密中
def count_CI2(cipher,n):     # n 代表我们猜测的秘钥，也即偏移量
    N = [0.0 for i in range(26)]
    cipher = c_alpha(cipher)
    L = len(cipher)
    #计算字符出现频数
    for i in cipher:
        N[(ascii_lowercase.index(i) - n + 26)%26] += 1

    CI_2 = 0
    for i in range(26):
        CI_2 += ((N[i] / L) * F[i])  #此处与上面不同  *重合指数公式2*
    return CI_2


## 找出单个分组的前5个最可能的单个秘钥
def pre_5_key(cipher):
    M = [(0,0.0) for i in range(26)]
    for i in range(26):
        M[i] = (chr(ord('a')+i),abs(0.065 - count_CI2(cipher,i)))
    M = sorted(M,key = lambda x:x[1])   #按照数组第二个元素排序
    for i in range(5):
        print (M[i])

# 得到密钥猜测值
def target_key(cipher,key_len):
    un_cip = ['' for i in range(key_len)]
    cipher_alpha = c_alpha(cipher)
    for i in range(len(cipher_alpha)):     # 完成分组工作
        z = i % key_len
        un_cip[z] += cipher_alpha[i]

    print("\n\n\n猜测密钥:")
    for i in range(key_len):
        print (i)
        pre_5_key(un_cip[i])     #这里将每个分组的5个最可能秘钥猜测全部打印出来



if __name__ == "__main__":
    cipher = 'faprepeapmsstwmcxdfwfaprepeapmsstwmcxdfwfaprepeapmsstwmcxdfwfaprepeapmsstwmcxdfwfaprepeapmsstwmcxdfwdteprdxcrsnlwtghealcegnzyahzeleutgircdgebpawxhpidtogidiqjxaqecixektglhispdwanhavokxoisiwpylixxetthzgctgpbptgtinrttwucrzrtgdwpaqapxodqtkogyfwthxxtlnheypxseleqpwpaahzlahxewfpcdpiztprgapyhsspgmdqtnohpbmythdqeriwpcsttxxowpgibttysuicfqbtgphbnrcmtxrdedxslwspndxhtqlplheweswtoaiiwrslsrzpogxykihffmtthtqpaneleqtdxagdfrdetcgecixsrtpngugpeitwpyxhtqlpljhphaiucenrtelaczdxobtemcjazysitdxicvmcsrxprtxhewicvpvmpcjxhtizrgjteaihitrgcpeyrtdqmthrzrttcewcdcqmrbhelaiisiwdgwhcjemelawlwcdbpeldcraanucsmiwppepisirpcopartdzagxpxyiwlxwphnsmbdyesgtniniajesiwpwtwtqivtgysvphdicgteedxslwspndmsxidvasxnelantqpgdgidhnyxaritgfdpxensjymqjtvriiiphrphnleaulfrxrrmvtcelaiismsxhdypeddididxektisibpawjahipvacsavokxoitwtqvetztgkhepgipatwthatoeqtnohpbhmtwbzveedhirxixeycdefehjctrxhtrgiwlxgdpwoetepvsaxvibjuqsnpgpynwpatyhelmnvdlpkttairetovordyxrtglwspxoxhtqlmlprewsiglrgtajahxaphacxdlkttairiwzqahhzvechprasbtxttsrpodbtpyiwlxiilzylsecsbpqwcrthfptxcxsrthaicipnylpgrsaahlwavdlpkttairndflakteslxkpaiiweleupnxtwpexhtbloeghnvepipfaaadjogisibtcpjiidqwtgxvirhwpwaxsmifdgppepktrgrdainwprinudcwojisoogtlfuidfxfxtwhpapjirhwlzepadswtxrlesxyaiiwnviixnmsbblryhpjmnvisibpawmsidzpivweensisirtuzvewpchtdrzrtgdwmthqtkacstxsidzpivwenaepywjxytrelhlkecrjuudiphbgpkmlxpyjogllvdtstpsdclwspntrgtpcpitgelihbzrtwlsmltheviztcvikpwhohpthiihzertsesoupcahtcvmcztonojgyelxhewaiisimpxytrthdgeciciicnzoowpxehpkpfetcrmvtcelerwlrctizxrndfxtwtqivtgysvpucsmiwptecpwxyhezxwxisxhtptqouwtxtxcrwptrtelipckeihtrtwtrsaahzjagupahpkpfetclfltizwcdgpqogtelacutzedjesfityeliwzygwismsbpjlaktwmtiapxosdhmtwisiqjpwmtndqxhtqlplejedasbtxsiwlxtwtmelaxdsniwppivwewistzjfxulwtdvcemlttkhigpuuxgpqecimythpjwiixdroqxrkegisenegpzidjdfaaadxhtrzrtgdgirhnzzegisibpawelhdsespczjfexeghsxxinhxzricsfwtgntrsxspvshpjmtbpjfecdnsicrthecrpxhpiapantcwfgdxfrpotpsedywogtofypsthahgtzaactoewpgibttyemdcrxhtqlplhbzwtkdnmftgzysrgtxirhelehpximxvsxgduzvtwtavaxhphihwphojiqsriwpfaaamcbtrvlabdyiouisimpxytlpnpvsjhphtdecsmdipedxslwefjttmtce'
    pre_10(cipher)
    key_len = 5  # 输入猜测的秘钥长度
    target_key(cipher, key_len)
