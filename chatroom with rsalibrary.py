import socket
import threading
import rsa

public_key,private_key = rsa.newkeys(1024)
public_partner = "None"
def sendmsg(c):
    while True:
        msg = input("")
        c.send(rsa.encrypt(msg.encode(),public_partner))
        print("You: " + msg)

def receivemsg(c):
    while True:
        # msg = c.recv(1024).decode()
        print("Partner: " + rsa.decrypt(c.recv(1024),private_key).decode())

choice = input("Do you want to host(1) or connect(2): ")

if choice == "1":                # hosting client
    # Hosting the server SOCK_STREAM for TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("192.168.1.134", 9999))
    server.listen()
    print("Server is listening...")

    client, _ = server.accept()
    client.send(public_key.save_pkcs1("PEM"))  # ENCODED TO DER FORMAT  bytes    # Hosting client is gonna send the public  key and  receive 
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
    print("Client connected.")

elif choice == "2":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # first receive public key then send
    client.connect(("192.168.1.134", 9999))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
    client.send(public_key.save_pkcs1("PEM"))
    print("Connected to server.")
else:
    exit()
threading.Thread(target=sendmsg, args=(client,)).start()
threading.Thread(target=receivemsg, args=(client,)).start()
