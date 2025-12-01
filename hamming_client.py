import socket, random

def calc_parity(data, pos):
    p = 0
    for i in range(1, len(data)):
        if (i & pos) == pos and i != pos:
            p ^= data[i]
    return p

def gen_hamming(msg):
    r = 1
    while 2**r < len(msg) + r + 1:
        r += 1
    code = [0] * (len(msg) + r + 1)
    j = 0
    for i in range(1, len(code)):
        if (i & (i-1)) != 0:
            code[i] = int(msg[j])
            j += 1
    for i in range(r):
        pos = 2**i
        code[pos] = calc_parity(code, pos)
    return code

def introduce_error(code):
    bit = random.randint(1, len(code)-1)
    code[bit] = 1 - code[bit]
    print(f"Error introduced at position {bit}")
    return bit

s = socket.socket()
s.connect(('127.0.0.1', 5000))

msg = input("Enter binary number: ")
hamming_code = gen_hamming(msg)
print("Generated Hamming Code:", "".join(map(str, hamming_code[1:])))

if input("Introduce error? (y/n): ").lower() == 'y':
    introduce_error(hamming_code)
    print("Corrupted Hamming Code:", "".join(map(str, hamming_code[1:])))


s.send("".join(map(str, hamming_code[1:])).encode())


ack = s.recv(1024).decode()
print("Server response:", ack)
s.close()
