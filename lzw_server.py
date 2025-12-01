import socket

def lzw_decompress(data):
    codes = [int(x) for x in data.split("#")]
    dictionary, dict_size = {i: chr(i) for i in range(256)}, 256
    w = chr(codes[0])
    result = [w]
    for k in codes[1:]:
        entry = dictionary[k] if k in dictionary else w + w[0]
        result.append(entry)
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
        w = entry
    return "".join(result)

s = socket.socket()
s.bind(('127.0.0.1', 65433))
s.listen(1)
print("Server listening...")

conn, addr = s.accept()
print("Connected by", addr)

while True:
    data = conn.recv(1024).decode()
    if not data:
        break
    print("Compressed data:", data)
    print("Decompressed:", lzw_decompress(data))

conn.close()
s.close()