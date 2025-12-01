import socket
import threading

clients = []

def handle_client(conn, addr):
    print(f"Connected with: {addr}")
    while True:
        data = conn.recv(1024).decode()
        if not data:  
            break
        print(f"{addr} says: {data}")
        
        for client in clients:
            if client != conn:
                client.send(data.encode())
    conn.close()
    clients.remove(conn)
    print(f"Connection with {addr} closed.")


s = socket.socket()
s.bind(('127.0.0.1', 5000))
s.listen(5)
print("Server started on 127.0.0.1:5000")

while True:
    conn, addr = s.accept()
    clients.append(conn)
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
