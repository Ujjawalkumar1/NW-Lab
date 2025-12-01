import socket

s = socket.socket()
s.connect(('127.0.0.1', 5000))

while True:
    msg = input()
    if msg == 'exit':
        break
    s.send(msg.encode())
    data = s.recv(1024).decode()
    print(data)

s.close()
