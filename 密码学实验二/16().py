import os
import re
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Generate a random AES key
AES_KEY = os.urandom(16)

# Predefined strings to prepend and append
PREPEND_STRING = "comment1=cooking%20MCs;userdata="
APPEND_STRING = ";comment2=%20like%20a%20pound%20of%20bacon"

# Function to sanitize input and escape ";" and "=" characters
def sanitize_input(user_input: str) -> str:
    return user_input.replace(";", "%3B").replace("=", "%3D")

# Function to encrypt the input string
def encrypt_userdata(user_input: str) -> bytes:
    sanitized_input = sanitize_input(user_input)
    data_to_encrypt = PREPEND_STRING + sanitized_input + APPEND_STRING
    
    # Pad to 16-byte AES block size
    padded_data = pad(data_to_encrypt.encode(), AES.block_size)
    
    # Generate random IV for CBC mode
    iv = os.urandom(16)
    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
    
    # Encrypt the data
    ciphertext = cipher.encrypt(padded_data)
    
    # Return IV + ciphertext
    return iv + ciphertext

# Function to decrypt the data and check for ";admin=true;"
def is_admin(ciphertext: bytes) -> bool:
    # Extract the IV from the ciphertext
    iv, encrypted_data = ciphertext[:16], ciphertext[16:]
    
    # Create a new AES cipher object with the extracted IV
    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
    
    # Decrypt the ciphertext
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    
    # Check if ";admin=true;" is present in the decrypted string
    return b";admin=true;" in decrypted_data

# Function to modify ciphertext to insert ";admin=true;" using CBC bit-flipping attack
def bitflip_attack(ciphertext: bytes) -> bytes:
    # We know the structure of the prepended data:
    # "comment1=cooking%20MCs;userdata="
    # We can inject our desired ";admin=true;" by flipping bits in the IV
    block_size = AES.block_size
    iv = list(ciphertext[:block_size])  # Convert to mutable list for manipulation
    
    # We want to modify the first block of user input in the second block of plaintext
    # Assume user_input starts from the second block, modify it to ";admin=true;"
    
    # XOR manipulation to flip bits in the IV to achieve desired outcome
    target_plaintext = b";admin=true;"
    start_idx = len(PREPEND_STRING)  # Start index in the second block
    
    for i in range(len(target_plaintext)):
        iv[start_idx + i] ^= ord("?") ^ target_plaintext[i]  # Example attack
    
    # Return modified ciphertext
    modified_iv = bytes(iv)
    return modified_iv + ciphertext[block_size:]

# Main function to test the attack
def main():
    # Encrypt some benign input
    user_input = "random_input"
    ciphertext = encrypt_userdata(user_input)
    
    print(f"Original ciphertext: {ciphertext.hex()}")
    
    # Attempt bit-flipping attack
    modified_ciphertext = bitflip_attack(ciphertext)
    
    print(f"Modified ciphertext: {modified_ciphertext.hex()}")
    
    # Check if admin privileges are granted
    if is_admin(modified_ciphertext):
        print("Success: Admin access granted!")
    else:
        print("Failure: Admin access not granted.")

if __name__ == "__main__":
    main()
