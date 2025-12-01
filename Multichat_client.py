import socket
import threading

def receive_messages(s):
    while True:
        data = s.recv(1024).decode()
        if not data:
            break
        print("Message:", data)


s = socket.socket()
s.connect(('127.0.0.1', 5000))
print("Connected to server. Type messages:")


thread = threading.Thread(target=receive_messages, args=(s,))
thread.daemon = True
thread.start()


while True:
    msg = input()
    s.send(msg.encode())
    if msg.lower() == 'bye':
        break

s.close()


