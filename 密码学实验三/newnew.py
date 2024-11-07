import random
from sympy import isprime, nextprime

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(e, et):
    gcd, x, y = extended_gcd(e, et)
    if gcd != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % et

def generate_prime(bits):
    while True:
        p = random.getrandbits(bits)
        if isprime(p):
            return p

def generate_keys(bits=512):
    p = generate_prime(bits)
    q = generate_prime(bits)
    n = p * q
    et = (p - 1) * (q - 1)
    e = 3
    d = mod_inverse(e, et)
    return (e, n), (d, n)

def encrypt(m, public_key):
    e, n = public_key
    return pow(m, e, n)

def decrypt(c, private_key):
    d, n = private_key
    return pow(c, d, n)

def string_to_number(s):
    return int(s.encode('utf-8').hex(), 16)

def number_to_string(n):
    return bytes.fromhex(hex(n)[2:]).decode('utf-8')

# Test the RSA implementation with small primes
public_key, private_key = generate_keys(bits=10)  # Use smaller bits for testing
print("Public Key:", public_key)
print("Private Key:", private_key)

message = 42
print("Original Message:", message)

encrypted_message = encrypt(message, public_key)
print("Encrypted Message:", encrypted_message)

decrypted_message = decrypt(encrypted_message, private_key)
print("Decrypted Message:", decrypted_message)

# Test the RSA implementation with string encryption/decryption
test_string = "Hello, RSA!"
print("Original String:", test_string)

number_representation = string_to_number(test_string)
print("String as Number:", number_representation)

encrypted_number = encrypt(number_representation, public_key)
print("Encrypted Number:", encrypted_number)

decrypted_number = decrypt(encrypted_number, private_key)
print("Decrypted Number:", decrypted_number)

decrypted_string = number_to_string(decrypted_number)
print("Decrypted String:", decrypted_string)
