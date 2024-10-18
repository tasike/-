def xor_with_repeating_key(repeating_key, input_text):
    key_length = len(repeating_key)
    encrypted_chars = []
    
    for index, char in enumerate(input_text):
        key_index = index % key_length
        encrypted_char = chr(ord(repeating_key[key_index]) ^ ord(char))
        encrypted_chars.append(encrypted_char)
    
    return ''.join(encrypted_chars)

def main():
    p1 = "Burning 'em, if you ain't quick and nimbleI go crazy when I hear a cymbal"
    key = 'ICE'
    
    c1 = xor_with_repeating_key(key, p1)
    c1_hex = c1.encode('utf-8').hex()
    
    print(c1_hex)

if __name__ == '__main__':
    main()