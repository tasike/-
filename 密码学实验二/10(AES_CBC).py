import base64  
from Crypto.Cipher import AES

def is_pkcs7_padded(data: bytes) -> bool:
    padding_length = data[-1]
    padding = data[-padding_length:]
    return all(byte == padding_length for byte in padding)

def remove_pkcs7_padding(data: bytes) -> bytes:
    if is_pkcs7_padded(data):
        padding_length = data[-1]
        return data[:-padding_length]
    return data

def decrypt_aes_ecb(cipher: bytes, aes_key: bytes) -> bytes:
    cipher_temp = AES.new(aes_key, AES.MODE_ECB)
    decrypted_data = cipher_temp.decrypt(cipher)
    return remove_pkcs7_padding(decrypted_data)

def decrypt_aes_cbc(cipher:bytes, aes_key:bytes, iv_vector:bytes) -> bytes:
    plain = b''
    block_size = len(aes_key)
    pre_vector = iv_vector
    for i in range(0, len(cipher), block_size): 
        decrypted_block = decrypt_aes_ecb(cipher[i:i + block_size], aes_key)
        plain_block = bytes(b1 ^ b2 for b1, b2 in zip(decrypted_block, pre_vector))
        plain += plain_block
        pre_vector = cipher[i:i + block_size]
    return plain

def main():
    with open('10.txt') as f:
        cipher_bytes = base64.b64decode(f.read())
    aes_key = b'YELLOW SUBMARINE'
    iv_vector = b'\x00' * AES.block_size
    plain_bytes = decrypt_aes_cbc(cipher_bytes, aes_key, iv_vector)
    print(plain_bytes.decode("utf-8"))

if __name__ == "__main__":
    main()