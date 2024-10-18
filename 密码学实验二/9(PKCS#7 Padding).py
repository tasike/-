def pkcs7_padding(data, block_size):
    padding_length = block_size - (len(data) % block_size)    # 数据长度比块长度要短
    padding = bytes([padding_length]*padding_length)
    return data + padding

msg = b'YELLOW SUBMARINE'
block_size = 20
padded_msg = pkcs7_padding(msg, block_size)
print(padded_msg)