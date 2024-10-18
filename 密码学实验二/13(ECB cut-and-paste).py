from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

# PKCS7 padding
def pkcs7_padding(data, block_size=16):
    padding_length = block_size - (len(data) % block_size)
    padding = bytes([padding_length] * padding_length)
    return data + padding

# PKCS7 unpadding
def pkcs7_unpadding(data):
    padding_length = data[-1]
    return data[:-padding_length]

# AES ECB Encryption
def aes_encrypt_ecb(plaintext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_plaintext = pkcs7_padding(plaintext)
    return cipher.encrypt(padded_plaintext)

# AES ECB Decryption
def aes_decrypt_ecb(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(ciphertext)
    return pkcs7_unpadding(decrypted)

# Parsing k=v strings into a dictionary
def parse_kv_string(kv_string):
    pairs = kv_string.split('&')
    result = {}
    for pair in pairs:
        key, value = pair.split('=')
        result[key] = value
    return result

# Generate user profile
def profile_for(email):
    # Sanitize the email address by removing `&` and `=`
    email = email.replace('&', '').replace('=', '')
    return f"email={email}&uid=10&role=user"

# Find AES block size
def find_block_size(key):
    initial_len = len(aes_encrypt_ecb(b"", key))
    i = 1
    while True:
        plaintext = b"A" * i
        new_len = len(aes_encrypt_ecb(plaintext, key))
        if new_len > initial_len:
            return new_len - initial_len
        i += 1

# Craft admin profile using ECB block manipulation
def make_admin_profile(key, block_size):
    # Generate different profiles with crafted emails
    email1 = "foo@bar.com"
    email2 = "foobar@foo.com"
    email3 = "foooooo@foo."

    profile1 = profile_for(email1).encode()
    profile2 = profile_for(email2).encode()
    profile3 = profile_for(email3).encode()

    # Encrypt the profiles
    cipher1 = aes_encrypt_ecb(profile1, key)
    cipher2 = aes_encrypt_ecb(profile2, key)
    cipher3 = aes_encrypt_ecb(profile3, key)

    # Encrypt "admin" and craft the final block for manipulation
    admin_block = aes_encrypt_ecb(pkcs7_padding(b"admin"), key)

    # Replace the last block of the profile with the admin block
    crafted_ciphertext = cipher3[:-block_size] + admin_block

    # Decrypt crafted ciphertext to get the final profile
    decrypted = aes_decrypt_ecb(crafted_ciphertext, key)
    print(f"Decrypted crafted profile: {decrypted.decode()}")

# Main logic
if __name__ == "__main__":
    # Generate a random AES key
    key = get_random_bytes(16)

    # Find block size
    block_size = find_block_size(key)
    print(f"Block size: {block_size}")

    # Encrypt and print the admin profile
    make_admin_profile(key, block_size)
