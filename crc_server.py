import socket
import random

# Function to perform XOR operation
def xor(a, b):
    result = []
    for i in range(1, len(b)):
        result.append(str(int(a[i]) ^ int(b[i])))
    return ''.join(result)

# Function to perform CRC division
def crc_division(dividend, divisor):
    pick = len(divisor)
    tmp = dividend[0:pick]
    while pick < len(dividend):
        if tmp[0] == '1':
            tmp = xor(divisor, tmp) + dividend[pick]
        else:
            tmp = xor('0'*pick, tmp) + dividend[pick]
        pick += 1

    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0'*pick, tmp)
    return tmp

# Function to generate the encoded data (message + remainder)
def encode_data(data, key):
    l_key = len(key)
    appended_data = data + '0'*(l_key-1)
    remainder = crc_division(appended_data, key)
    codeword = data + remainder
    return codeword

# create socket
s = socket.socket()
s.bind(('127.0.0.1', 6000))
s.listen(1)
print("Server listening on port 6000...")

conn, addr = s.accept()
print(f"Connected by {addr}")

# receive message and key
msg = conn.recv(1024).decode()
key = conn.recv(1024).decode()

# encode data
encoded_no_error = encode_data(msg, key)
output = "\nOUTPUT\n"
output += f"Enter message: {msg}\nEnter the key: {key}\n\n"
output += f"Without error:\nEncoded Data (Data + Remainder): {encoded_no_error}\n"

# introduce random error
encoded_with_error = list(encoded_no_error)
pos = random.randint(0, len(encoded_with_error)-1)
encoded_with_error[pos] = '1' if encoded_with_error[pos] == '0' else '0'
encoded_with_error = ''.join(encoded_with_error)

output += f"\nWith error:\nEncoded Data (Data + Remainder): {encoded_with_error}"

# send to client
conn.send(output.encode())

conn.close()
s.close()
