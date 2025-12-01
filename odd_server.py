import socket

s = socket.socket()
s.bind(('127.0.0.1', 5000))
s.listen(1)

print("Server is listening on 127.0.0.1:5000...")

conn, addr = s.accept()
print("Connected with:", addr)

while True:
    data = conn.recv(1024).decode()
    if not data:
        break

    print("Received from client:", data)
    
    # Convert received data to integer
    num = int(data)
    
    
    # Check even or odd
    if num % 2 == 0:
        result = f"{num} is an even number"
    else:
        result = f"{num} is an odd number"

    # Send result back to client
    conn.send(result.encode())



conn.close()
s.close()






