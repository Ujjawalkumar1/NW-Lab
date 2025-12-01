# Diffie-Hellman Key Exchange - SERVER
import socket
import random

# Step 1: choose public numbers (can be known by everyone)
P = 23   # prime number
G = 9    # base (generator)

# Step 2: server chooses a private (secret) number
server_private = random.randint(1, P - 1)  # secret 'a'
server_public = pow(G, server_private, P)  # A = G^a mod P

print("Public P:", P)
print("Public G:", G)
print("Server private (secret):", server_private)
print("Server public value (A):", server_public)

# Step 3: create TCP socket and wait for client
s = socket.socket()
s.bind(('127.0.0.1', 5001))
s.listen(1)
print("Server listening on 127.0.0.1:5001")

conn, addr = s.accept()
print("Connected with:", addr)

# Step 4: send P, G and server_public (A) to client
data_to_send = str(P) + "," + str(G) + "," + str(server_public)
conn.send(data_to_send.encode())

# Step 5: receive client public value (B)
client_data = conn.recv(1024).decode()
client_public = int(client_data.strip())
print("Client public value (B):", client_public)

# Step 6: compute shared secret key: S = B^a mod P
shared_secret = pow(client_public, server_private, P)
print("Shared secret (server side):", shared_secret)

# Step 7: send a small confirmation message to client
conn.send("Shared secret established!".encode())

conn.close()
s.close()
