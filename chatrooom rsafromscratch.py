import socket
import threading
import random
import math

def is_prime(number):
    if number < 2:
        return False
    for i in range(2, int(math.sqrt(number)) + 1):
        if number % i == 0:
            return False
    return True

def generate_prime(min_value, max_value):            # generating prime numbers within a range.
    prime = random.randint(min_value, max_value)
    while not is_prime(prime):
        prime = random.randint(min_value, max_value)
    return prime

# Function to compute the modular inverse of e modulo phi
def mod_inverse(e, phi):
    for d in range(3, phi):
        if (d * e) % phi == 1:     # d is multiplicative inverse of e.
            return d
    raise ValueError("mod_inverse does not exist")

# Generating random prime numbers p and q. range is small for easier encryption and decryption
p = generate_prime(1000, 8000)
q = generate_prime(1000, 8000)
while p == q:
    q = generate_prime(1000, 8000)

#  n and Euler's totient function phi(n)
n = p * q
phi_n = (p - 1) * (q - 1)

# Generating public and private keys  
e = random.randint(3, phi_n - 1)        # public key is e and 3<=e<=phi_n-1
while math.gcd(e, phi_n) != 1:  # ensure e is coprime with phi_n
    e = random.randint(3, phi_n - 1)

d = mod_inverse(e, phi_n)                # d is the private key

# Function to encrypt a message into ciphertext
def encoding(message):
    encode = [ord(ch) for ch in message]  # Converting message to a list of Unicode code points
    cipher = [pow(ch, e, n) for ch in encode]  # Encrypting each code point
    return cipher

#  decrypting ciphertext back to plaintext
def decoding(cipher):
    decode = [pow(ch, d, n) for ch in cipher]  # Decrypt back to Unicode code points
    byte_array = bytearray()
    for num in decode:
        byte_array.extend(num.to_bytes((num.bit_length() + 7) // 8, byteorder='big'))  # taking out all versions - unicode , latin-1 and utf -8

    
    try:
        msg = byte_array.decode('utf-8')
    except UnicodeDecodeError:
        try:
            msg = byte_array.decode('latin-1')
        except UnicodeDecodeError:
            msg = ''.join(chr(byte) for byte in byte_array if byte < 128)  # Filtering  out non-ASCII characters
    return msg

# Placeholder for public key of partner
public_key = e
public_partner = None

# Function to send messages
def sendmsg(c):
    while True:
        msg = input("You: ")
        if msg.lower() == "exit":
            break
        en_msg = encoding(msg)
        c.send(str(en_msg).encode('utf-8'))

# Function to receive messages
def receivemsg(c):
    while True:
        encrypted_msg = c.recv(1024).decode('utf-8')
        if not encrypted_msg:
            continue
        cipher = eval(encrypted_msg)  # Converting  back to list using eval
        decrypted_msg = decoding(cipher)
        print("Partner:", decrypted_msg)
        print("")

# Prompting  user to host or connect
choice = input("Do you want to host(1) or connect(2): ")

if choice == "1":  # Hosting server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("192.168.1.134", 9999))  # my ip and usual port
    server.listen()
    print("Server is listening...")

    client, _ = server.accept()
    client.send(str(public_key).encode('utf-8'))  # Sending  public key to client
    public_partner = int(client.recv(1024).decode('utf-8'))  # Receiving  public key of client
    print("Client connected.")

elif choice == "2":  # Connecting client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("192.168.1.134", 9999))  # IP and port
    public_partner = int(client.recv(1024).decode('utf-8'))  # Receiving public key of server
    client.send(str(public_key).encode('utf-8'))  # Sending public key to server
    print("Connected to server.")

else:
    print("Invalid choice. Exiting...")
    

# Print RSA key details
    print("\nRSA Key Details:")
    print("Public key (e):", public_key)
    print("Private key (d):", d)
    print("n:", n)
    print("phi of n is:", phi_n)
    print("p:", p)
    print("q:", q)
    exit()
# Start threads for sending and receiving messages
threading.Thread(target=sendmsg, args=(client,)).start()
threading.Thread(target=receivemsg, args=(client,)).start()
