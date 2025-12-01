import socket

def calc_parity(data, pos):
    p = 0
    for i in range(1, len(data)):
        if (i & pos) == pos and i != pos:
            p ^= data[i]
    return p

def detect_error(code):
    pos = 1
    error_pos = 0
    while pos < len(code):
        if calc_parity(code, pos) != code[pos]:
            error_pos += pos
        pos *= 2
    return error_pos

def decode_hamming(code):
    decoded = []
    for i in range(1, len(code)):
        if (i & (i-1)) != 0:
            decoded.append(str(code[i]))
    return "".join(decoded)

s = socket.socket()
s.bind(('127.0.0.1', 5000))
s.listen(1)
print("Server listening on port 5000")

conn, addr = s.accept()
print(f"Connected by {addr}")

code = list(map(int, conn.recv(1024).decode()))
print("Received Hamming Code:", "".join(map(str, code)))

error_pos = detect_error([0] + code)
if error_pos == 0:
    print("No errors detected.")
    response = "No errors detected"
else:
    print(f"Error detected at position {error_pos}")
    response = f"Error detected at position {error_pos}"

decoded = decode_hamming([0] + code)
print("Decoded Data:", decoded)

conn.send(response.encode())
conn.close()
s.close()
