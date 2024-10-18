
def hex_xor(s1, s2):  # 输入两个十六进制字符串
    len_s = len(s1) if len(s1) < len(s2) else len(s2)
    res = ''
    for i in range(0, len_s, 2):
        res += hex(int(s1[i:i+2],16)^int(s2[i:i+2],16))[2:]    # 此处切片[2:]的原因在于,hex将数字转换为16进制字符串之后会带有0x,比如hex(255)结果为'0xff',从而用切片你去掉0x
    return res
    
if __name__ == "__main__":
    s1 = '1c0111001f010100061a024b53535009181c'
    s2 = '686974207468652062756c6c277320657965'
    res = hex_xor(s1, s2)
    print(res)



