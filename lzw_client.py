import socket

def lzw_compress(text):
    dictionary = {chr(i): i for i in range(256)}
    dict_size, w, compressed = 256, "", ""
    for c in text:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            compressed += str(dictionary[w]) + "#"
            dictionary[wc] = dict_size
            dict_size += 1
            w = c
    if w:
        compressed += str(dictionary[w]) + "#"
    return compressed[:-1]

s = socket.socket()
s.connect(('127.0.0.1', 65433))

while True:
    msg = input("Enter plain text: ")
    compressed = lzw_compress(msg)
    print("Compressed:", compressed)
    s.send(compressed.encode())
