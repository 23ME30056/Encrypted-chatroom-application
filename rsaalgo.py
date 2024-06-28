import random
import math

def is_prime(number):
    if number < 2:
        return False
    count = 0
    for i in range(1, number+1):
        if number % i == 0:
            count += 1
    if count == 2:
        return True
    else:
        return False

def generate_prime(min_value, max_value):
    prime = random.randint(min_value, max_value)
    while not is_prime(prime):
        prime = random.randint(min_value, max_value)
    return prime

def mod_inverse(e, phi):
    for d in range(3, phi):
        if (d * e) % phi == 1:  # generating multiplicative inverse of e
            return d
    raise ValueError("mod_inverse does not exist")

p = generate_prime(1000, 8000)   # random numbers
q = generate_prime(1000, 8000)
while p == q:
    q = generate_prime(1000, 8000)

n = p * q
phi_n = (p - 1) * (q - 1)

e = random.randint(3, phi_n - 1)
while math.gcd(e, phi_n) != 1:                   # generating coprime numbers
    e = random.randint(3, phi_n - 1)

d = mod_inverse(e, phi_n)

print("Public key:", e)                   # 
print("Private key:", d)
print("n:", n)
print("phi of n is:", phi_n)
print("p:", p)
print("q:", q)

message = "Hi baby girl"
encode = [ord(ch) for ch in message]
cipher = [pow(ch, e, n) for ch in encode]  # encrypt it to cipher    # c = m^e mod n
print("Cipher text:", cipher)

decode = [pow(ch, d, n) for ch in cipher]  # decrypt back to ASCII  # m = c^d mod n
msg = "".join(chr(ch) for ch in decode)
print("Decrypted message:", msg)
