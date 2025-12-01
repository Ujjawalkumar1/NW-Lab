# Diffie-Hellman Key Exchange - CLIENT
import socket
import random

# Step 1: create socket and connect to server
s = socket.socket()
s.connect(('127.0.0.1', 5001))

# Step 2: receive P, G and server_public (A) from server
data = s.recv(1024).decode()
P_str, G_str, server_pub_str = data.strip().split(",")

P = int(P_str)
G = int(G_str)
server_public = int(server_pub_str)

print("Received P:", P)
print("Received G:", G)
print("Received server public (A):", server_public)

# Step 3: client chooses private (secret) number
client_private = random.randint(1, P - 1)  # secret 'b'
client_public = pow(G, client_private, P)  # B = G^b mod P

print("Client private (secret):", client_private)
print("Client public value (B):", client_public)

# Step 4: send client_public (B) to server
s.send(str(client_public).encode())

# Step 5: compute shared secret key: S = A^b mod P
shared_secret = pow(server_public, client_private, P)
print("Shared secret (client side):", shared_secret)

# Step 6: receive confirmation from server
msg = s.recv(1024).decode()
print("Server says:", msg)

s.close()
