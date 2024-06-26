import random
from sympy import isprime, mod_inverse

def generate_large_prime(keysize=1024):
    while True:
        num = random.getrandbits(keysize)
        if isprime(num):
            return num

def generate_keypair(keysize):
    p = generate_large_prime(keysize)
    q = generate_large_prime(keysize)
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    
    d = mod_inverse(e, phi)
    
    return ((e, n), (d, n))

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def encrypt(pk, plaintext):
    key, n = pk
    cipher = [(ord(char) ** key) % n for char in plaintext]
    return cipher

def decrypt(pk, ciphertext):
    key, n = pk
    plain = [chr((char ** key) % n) for char in ciphertext]
    return ''.join(plain)

# Generating public and private keys
public, private = generate_keypair(8)  # Using 8 bits for simplicity; use 1024 or 2048 bits for real applications
print("Public key:", public)
print("Private key:", private)

# Encrypting a message
message = "hello"
encrypted_msg = encrypt(public, message)
print("Encrypted message:", encrypted_msg)

# Decrypting the message
decrypted_msg = decrypt(private, encrypted_msg)
print("Decrypted message:", decrypted_msg)