import socket

# create socket
s = socket.socket()
s.connect(('127.0.0.1', 6000))

# input message and key
msg = input("Enter message: ")
key = input("Enter the key: ")

# send to server
s.send(msg.encode())
s.send(key.encode())

# receive and print results
data = s.recv(1024).decode()
print(data)

s.close()
