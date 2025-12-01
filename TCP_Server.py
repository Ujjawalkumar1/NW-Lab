import socket

s = socket.socket()
s.bind(('127.0.0.1', 5000))
s.listen(1)
conn, addr = s.accept()

while True:
    data = conn.recv(1024).decode()
    print(data)
    if not data:
        break
    conn.send(data.encode())

conn.close()
s.close()
