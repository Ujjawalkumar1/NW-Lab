import socket

s = socket.socket()
s.connect(('localhost', 60014))

key = input("Enter key: ")
s.send(key.encode())

msg = input("Enter message: ")
s.send(msg.encode())

cipher = s.recv(1024).decode()
print("Cipher text:", cipher)
s.close()
