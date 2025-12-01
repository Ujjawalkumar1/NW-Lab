import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    msg = input()
    if msg == 'exit':
        break
    s.sendto(msg.encode(), ('127.0.0.1', 5000))
    data, addr = s.recvfrom(1024)
    print(data.decode())

s.close()
