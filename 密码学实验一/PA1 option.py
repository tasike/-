import string 

cipher = 'F96DE8C227A259C87EE1DA2AED57C93FE5DA36ED4EC87EF2C63AAE5B9A7EFFD673BE4ACF7BE8923CAB1ECE7AF2DA3DA44FCF7AE29235A24C963FF0DF3CA3599A70E5DA36BF1ECE77F8DC34BE129A6CF4D126BF5B9A7CFEDF3EB850D37CF0C63AA2509A76FF9227A55B9A6FE3D720A850D97AB1DD35ED5FCE6BF0D138A84CC931B1F121B44ECE70F6C032BD56C33FF9D320ED5CDF7AFF9226BE5BDE3FF7DD21ED56CF71F5C036A94D963FF8D473A351CE3FE5DA3CB84DDB71F5C17FED51DC3FE8D732BF4D963FF3C727ED4AC87EF5DB27A451D47EFD9230BF47CA6BFEC12ABE4ADF72E29224A84CDF3FF5D720A459D47AF59232A35A9A7AE7D33FB85FCE7AF5923AA31EDB3FF7D33ABF52C33FF0D673A551D93FFCD33DA35BC831B1F43CBF1EDF67F0DF23A15B963FE5DA36ED68D378F4DC36BF5B9A7AFFD121B44ECE76FEDC73BE5DD27AFCD773BA5FC93FE5DA3CB859D26BB1C63CED5CDF3FE2D730B84CDF3FF7DD21ED5ADF7CF0D636BE1EDB79E5D721ED57CE3FE6D320ED57D469F4DC27A85A963FF3C727ED49DF3FFFDD24ED55D470E69E73AC50DE3FE5DA3ABE1EDF67F4C030A44DDF3FF5D73EA250C96BE3D327A84D963FE5DA32B91ED36BB1D132A31ED87AB1D021A255DF71B1C436BF479A7AF0C13AA14794'
vis_char_list = string.ascii_letters + string.digits + ',' + '.' + ' '  # 即'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,. '(注意最后一个是空格)

def i_of_key(cipher_same_pst_list):  # 找出key第i个位置的可能值,输出所有可能值的序列
    res = [i for i in range(0x00, 0xFF+1)]
    for key_byte in range(0x00, 0xFF+1):
        for cipher_byte in cipher_same_pst_list:
            if chr(cipher_byte^key_byte) not in vis_char_list:
                res.remove(key_byte)
                break
    return res

cipher_byte_list = []
for i in range(0, len(cipher), 2):
    cipher_byte_list.append(int(cipher[i:i+2], 16))  # 把字符串类型的十六进制转成int类型(如'61'->97)
for key_len in range(1, 13+1):
    for i in range(1, key_len+1):
        cipher_same_pst_list = cipher_byte_list[(i-1)::key_len]
        i_psb_key_list = i_of_key(cipher_same_pst_list)
        print('key_len=',key_len,',',i,'th of key possible=',i_psb_key_list)

# 观察上述的输出可以发现,密钥长度为7,并且每个位置的可能值都刚好为1个,因此直接得到了密钥
#   key_len= 7 , 1 th of key possible= [186]
#   key_len= 7 , 2 th of key possible= [31]
#   key_len= 7 , 3 th of key possible= [145]
#   key_len= 7 , 4 th of key possible= [178]
#   key_len= 7 , 5 th of key possible= [83]
#   key_len= 7 , 6 th of key possible= [205]
#   key_len= 7 , 7 th of key possible= [62]

key_len = 7
key_byte_list = [186, 31, 145, 178, 83, 205, 62]
plain = ''
for i in range(0, len(cipher_byte_list)):
    plain += chr(key_byte_list[i % key_len] ^ cipher_byte_list[i])
print('****************************************************')
key_hex = ''.join(format(x,'02x') for x in key_byte_list)
print('key:',key_hex)

print('The plain is:')
print(plain)




