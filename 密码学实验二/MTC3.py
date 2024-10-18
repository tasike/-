from hashlib import sha1
import codecs
import base64
from Crypto.Cipher import AES
import binascii

# #
# a = [1,1,1,1,1,6]
# b = [7,3,1,7,3,1]
# for i in range(0,6):
#     c = c + a[i]*b[i]
#     res = c % 10
# print (res)
# #res = 7
# ‘12345678<8<<<1110182<1111167<<<<<<<<<<<<<<<4’

def get_kseed()->str:
    MRZ_information = "12345678<811101821111167"
    H_mrz=sha1(MRZ_information.encode()).hexdigest()
    kseed=H_mrz[:32]
    return kseed

def get_kab(kseed:str):
    c = '00000001'
    m = kseed+c
    #先变为二进制散列再换成十六进制
    H_m=sha1(bytes.fromhex(m)).hexdigest()
    ka = H_m[:16]
    kb = H_m[16:32]
    return ka,kb

def get_jiou(n):
    k=[]
    n_bin=bin(int(n,16))[2:]
    for i in range(0,len(n_bin),8):
        if(n_bin[i:i+7].count("1"))%2 == 0:
            k.append(n_bin[i:i+7])
            k.append('1')
        else:
            k.append(n_bin[i:i+7])
            k.append('0')
    m=hex(int(''.join(k),2))[2:]
    return m


    
kseed=get_kseed()
ka,kb=get_kab(kseed)
k1=get_jiou(ka)
k2=get_jiou(kb)
key=k1+k2
print("*******************************************")
print("The Key is:",key)
print("*******************************************")
# 待解密的密文  
ciphertext = base64.b64decode(  
    "9MgYwmuPrjiecPMx61O6zIuy3MtIXQQ0E59T3xB6u0Gyf1gYs2i3K9Jxaa0zj4gTMazJuApwd6+jdyeI5iGHvhQyDHGVlAuYTgJrbFDrfB22Fpil2NfNnWFBTXyf7SDI")  
IV = '0' * 32  # 初始化向量  
  
# 使用AES进行解密  
m = AES.new(binascii.unhexlify(key), AES.MODE_CBC, binascii.unhexlify(IV)).decrypt(ciphertext)  
print(m.decode())  # 输出解密后的明文  