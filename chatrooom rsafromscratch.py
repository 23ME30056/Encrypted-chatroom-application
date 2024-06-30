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

def generate_prime(min_value, max_value):
    prime = random.randint(min_value, max_value)
    while not is_prime(prime):
        prime = random.randint(min_value, max_value)
    return prime

def mod_inverse(e, phi):
    for d in range(3, phi):
        if (d * e) % phi == 1:
            return d
    raise ValueError("mod_inverse does not exist")

# Generate random prime numbers p and q
p = generate_prime(100, 800)
q = generate_prime(100, 800)
while p == q:
    q = generate_prime(100, 800)

# Calculate n and Euler's totient function phi(n)
n = p * q
phi_n = (p - 1) * (q - 1)

# Generate public and private keys
e = random.randint(3, phi_n - 1)
while math.gcd(e, phi_n) != 1:  # ensure e is coprime with phi_n
    e = random.randint(3, phi_n - 1)

d = mod_inverse(e, phi_n)

# Function to encrypt a message into ciphertext
def encoding(message):
    encode = [ord(ch) for ch in message]
    cipher = [pow(ch, e, n) for ch in encode]  # encrypt it to cipher
    return cipher

# Function to decrypt ciphertext back to plaintext
def decoding(cipher):
    decode = [pow(ch, d, n) for ch in cipher]  # decrypt back to ASCII
    byte_array = bytearray()
    for num in decode:
        byte_array.extend(num.to_bytes((num.bit_length() + 7) // 8, byteorder='big'))
    msg = byte_array.decode('utf-8')
    return msg
public_key = e
public_partner = None  # Placeholder for public key of partner

# Function to send messages
def sendmsg(c):
    while True:
        msg = input("You: ")
        if msg.lower() == "exit":
            break
        en_msg = encoding(msg)
        c.send(bytes(str(en_msg), 'utf-8'))

# Function to receive messages
def receivemsg(c):
    while True:
        encrypted_msg = c.recv(1024).decode('utf-8')
        if not encrypted_msg:
            continue
        cipher = eval(encrypted_msg)  # Convert back to list using eval
        decrypted_msg = decoding(cipher)
        print("Partner: " + decrypted_msg)
        print("")

# Prompt user to host or connect
choice = input("Do you want to host(1) or connect(2): ")

if choice == "1":  # Hosting server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("192.168.1.134", 9999))
    server.listen()
    print("Server is listening...")

    client, _ = server.accept()
    client.send(str(public_key).encode('utf-8'))  # Send public key to client
    public_partner = int(client.recv(1024).decode('utf-8'))  # Receive public key of client
    print("Client connected.")

elif choice == "2":  # Connecting client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("192.168.1.134", 9999))
    public_partner = int(client.recv(1024).decode('utf-8'))  # Receive public key of server
    client.send(str(public_key).encode('utf-8'))  # Send public key to server
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