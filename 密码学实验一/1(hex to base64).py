
def base64_coding_table(itg):  # base64编码表,将码值转换为字符
    if itg in range(0, 26):
        return chr(itg+65)
    elif itg in range(26, 52):
        return chr(itg+71)
    elif itg in range(52, 62):
        return chr(itg-4)
    elif itg == 62:
        return '+'
    else:
        return '/'


def bese64_encoder(string):    # 输入为16进制字符串,二进制中左移是末尾添加0,右移是去末尾
    flag = int(len(string) /2) %3   # 用于标记分组后最后一组剩余几个字节
    string_int_list = []
    for i in range(0, len(string), 6):  # 注意这里要每隔6取
        string_int_list.append(int(string[i:i+6],16))   # 每3个字节为一组,也就是24个字节
    print(string_int_list)
    res = ''
    for i in range(0, len(string_int_list)):  # 先考虑正常也就是每组都是3个字节,最后一组是1个字节或2个字节最后单独考虑.
        group = string_int_list[i]
        if i == len(string_int_list)-1 and flag == 2:
            itg1 = (group >> 10) & 0x3F 
            itg2 = (group >> 4) & 0x3F
            itg3 = (group << 2) & 0x3F
            res += base64_coding_table(itg1)+base64_coding_table(itg2)+base64_coding_table(itg3)+'='
        elif i == len(string_int_list)-1 and flag == 1:
            itg1 = (group >> 2) & 0x3F 
            itg2 = (group << 4) & 0x3F
            res += base64_coding_table(itg1)+base64_coding_table(itg2)+'=='
        else:
            itg1 = (group >> 18) & 0x3F       # 依次提取每6位得到码值
            itg2 = (group >> 12) & 0x3F
            itg3 = (group >> 6) & 0x3F
            itg4 = group & 0x3F
            res += base64_coding_table(itg1)+base64_coding_table(itg2)+base64_coding_table(itg3)+base64_coding_table(itg4)
    return res

if __name__ == "__main__":
    string = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
    string_base64 = bese64_encoder(string)
    print(string_base64)

