import socket

s = socket.socket()
s.connect(('127.0.0.1', 5000))

while True:
    num = input("Enter a number (or 'exit' to quit): ")
    if num.lower() == 'exit':
        break

    s.send(num.encode())
    data = s.recv(1024).decode()
    print("Message from server:", data)

s.close()
