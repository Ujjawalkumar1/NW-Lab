# Network Programming Lab - All Programs

This document contains all network programming programs organized for revision.

---

## 1. TCP PROGRAMS

### TCP Server

```python
import socket

s = socket.socket()
s.bind(('127.0.0.1', 5000))
s.listen(1)
conn, addr = s.accept()

while True:
    data = conn.recv(1024).decode()
    print(data)
    if not data:
        break
    conn.send(data.encode())

conn.close()
s.close()
```

### TCP Client

```python
import socket

s = socket.socket()
s.connect(('127.0.0.1', 5000))

while True:
    msg = input()
    if msg == 'exit':
        break
    s.send(msg.encode())
    data = s.recv(1024).decode()
    print(data)

s.close()
```

---

## 2. UDP PROGRAMS

### UDP Server

```python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 5000))

while True:
    data, addr = s.recvfrom(1024)
    print(data.decode())
    if not data:
        break
    s.sendto(data, addr)

s.close()
```

### UDP Client

```python
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
```

---

## 3. CRC (Cyclic Redundancy Check) PROGRAMS

### CRC Server

```python
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
```

### CRC Client

```python
import socket

# create socket
s = socket.socket()
s.connect(('127.0.0.1', 6000))

# input message and key
msg = input("Enter message: ")
key = input("Enter the key: ")

# send to server
s.send(msg.encode())
s.send(key.encode())

# receive and print results
data = s.recv(1024).decode()
print(data)

s.close()
```

---

## 4. DIFFIE-HELLMAN KEY EXCHANGE PROGRAMS

### Diffie-Hellman Server

```python
# Diffie-Hellman Key Exchange - SERVER
import socket
import random

# Step 1: choose public numbers (can be known by everyone)
P = 23   # prime number
G = 9    # base (generator)

# Step 2: server chooses a private (secret) number
server_private = random.randint(1, P - 1)  # secret 'a'
server_public = pow(G, server_private, P)  # A = G^a mod P

print("Public P:", P)
print("Public G:", G)
print("Server private (secret):", server_private)
print("Server public value (A):", server_public)

# Step 3: create TCP socket and wait for client
s = socket.socket()
s.bind(('127.0.0.1', 5001))
s.listen(1)
print("Server listening on 127.0.0.1:5001")

conn, addr = s.accept()
print("Connected with:", addr)

# Step 4: send P, G and server_public (A) to client
data_to_send = str(P) + "," + str(G) + "," + str(server_public)
conn.send(data_to_send.encode())

# Step 5: receive client public value (B)
client_data = conn.recv(1024).decode()
client_public = int(client_data.strip())
print("Client public value (B):", client_public)

# Step 6: compute shared secret key: S = B^a mod P
shared_secret = pow(client_public, server_private, P)
print("Shared secret (server side):", shared_secret)

# Step 7: send a small confirmation message to client
conn.send("Shared secret established!".encode())

conn.close()
s.close()
```

### Diffie-Hellman Client

```python
# Diffie-Hellman Key Exchange - CLIENT
import socket
import random

# Step 1: create socket and connect to server
s = socket.socket()
s.connect(('127.0.0.1', 5001))

# Step 2: receive P, G and server_public (A) from server
data = s.recv(1024).decode()
P_str, G_str, server_pub_str = data.strip().split(",")

P = int(P_str)
G = int(G_str)
server_public = int(server_pub_str)

print("Received P:", P)
print("Received G:", G)
print("Received server public (A):", server_public)

# Step 3: client chooses private (secret) number
client_private = random.randint(1, P - 1)  # secret 'b'
client_public = pow(G, client_private, P)  # B = G^b mod P

print("Client private (secret):", client_private)
print("Client public value (B):", client_public)

# Step 4: send client_public (B) to server
s.send(str(client_public).encode())

# Step 5: compute shared secret key: S = A^b mod P
shared_secret = pow(server_public, client_private, P)
print("Shared secret (client side):", shared_secret)

# Step 6: receive confirmation from server
msg = s.recv(1024).decode()
print("Server says:", msg)

s.close()
```

---

## 5. HAMMING CODE PROGRAMS

### Hamming Server

```python
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
```

### Hamming Client

```python
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
```

---

## 6. LZW COMPRESSION PROGRAMS

### LZW Server

```python
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
```

### LZW Client

```python
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
```

---

## 7. MULTICHAT PROGRAMS

### Multichat Server

```python
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
```

### Multichat Client

```python
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


```

---

## 8. ODD/EVEN NUMBER CHECK PROGRAMS

### Odd/Even Server

```python
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





```

### Odd/Even Client

```python
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
```

---

## 9. PLAYFAIR CIPHER PROGRAMS

### Playfair Server

```python
import socket


def search(mat, ch):
    for i in range(5):
        for j in range(5):
            if mat[i][j] == ch:
                return i, j
    return 0, 0


def preprocess_playfair(msg):
    msg = msg.lower().replace(" ", "").replace("j", "i")
    pairs = []
    i = 0
    while i < len(msg):
        a = msg[i]
        b = msg[i+1] if i+1 < len(msg) else 'x'
        if a == b:
            pairs.append(a+'x')
            i += 1
        else:
            pairs.append(a+b)
            i += 2
    return msg + ('x' if len(msg)%2 else ''), pairs


def encrypt(key, message):
    plain_text, digraphs = preprocess_playfair(message)
    letters = list('abcdefghiklmnopqrstuvwxyz')
    key_letters = []
    for ch in key.lower():
        if ch == 'j': ch = 'i'
        if ch not in key_letters and ch in letters:
            key_letters.append(ch)
    all_letters = key_letters + [c for c in letters if c not in key_letters]
    matrix = [all_letters[i:i+5] for i in range(0,25,5)]

    print(f"Plain text: {plain_text}")
    print(f"Digraphs: {digraphs}")
    print("Matrix:")
    for row in matrix:
        print(row)

    cipher = ""
    for a, b in digraphs:
        r1, c1 = search(matrix, a)
        r2, c2 = search(matrix, b)
        if r1 == r2:
            cipher += matrix[r1][(c1+1)%5] + matrix[r2][(c2+1)%5]
        elif c1 == c2:
            cipher += matrix[(r1+1)%5][c1] + matrix[(r2+1)%5][c2]
        else:
            cipher += matrix[r1][c2] + matrix[r2][c1]
    print(f"Cipher text: {cipher}")
    return cipher


s = socket.socket()
s.bind(('localhost', 60014))
s.listen(1)
print("Server listening on localhost:60014")

while True:
    conn, addr = s.accept()
    print(f"Connection from {addr}")
    key = conn.recv(1024).decode()
    message = conn.recv(1024).decode()
    print(f"Received key: {key}")
    print(f"Received message: {message}")
    cipher = encrypt(key, message)
    conn.send(cipher.encode())
    conn.close()



# We are creating a 5×5 matrix (list of lists) for the Playfair cipher.

# all_letters[i:i+5] → take a slice of 5 letters from all_letters, starting at index i.

# for i in range(0, 25, 5) → i takes values 0, 5, 10, 15, 20.

# So slices are:

# all_letters[0:5] → first row

# all_letters[5:10] → second row

# all_letters[10:15] → third row

# all_letters[15:20] → fourth row

# all_letters[20:25] → fifth row

# Example:
# If all_letters = ['m','o','n','a','r','c','h','y','b','d','e','f','g','i','k','l','p','q','s','t','u','v','w','x','z']

# matrix[0] → ['m','o','n','a','r']

# matrix[1] → ['c','h','y','b','d']

# matrix[2] → ['e','f','g','i','k']

# matrix[3] → ['l','p','q','s','t']

# matrix[4] → ['u','v','w','x','z']
```

### Playfair Client

```python
import socket

s = socket.socket()
s.connect(('localhost', 60014))

key = input("Enter key: ")
s.send(key.encode())

msg = input("Enter message: ")
s.send(msg.encode())

cipher = s.recv(1024).decode()
print("Cipher text:", cipher)
s.close()
```

---

## 10. RAILFENCE CIPHER PROGRAMS

### Railfence Server

```python
import socket

def decryptRailFence(cipher, key):
   
    rail = [['\n' for _ in range(len(cipher))] for _ in range(key)]
    row, col = 0, 0
    dir_down = None

    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
        rail[row][col] = '*' 
        col += 1
        if dir_down:
            row = row + 1
        else:
            row = row - 1


# *       *
#   *   *
#     *
            

    
    index = 0
    for i in range(key):
        for j in range(len(cipher)):
            if rail[i][j] == '*' and index < len(cipher):
                rail[i][j] = cipher[index]
                index += 1

    result = []
    row, col = 0, 0
    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
        if rail[row][col] != '\n':
            result.append(rail[row][col])
            col += 1
        if dir_down:
            row = row + 1
        else:
            row = row - 1

   
    return "".join(result)



s = socket.socket()
s.bind(('127.0.0.1', 65432))
s.listen(1)
print("Server is listening...")

conn, addr = s.accept()
print(f"Connected by {addr}")

while True:
    data = conn.recv(1024).decode()
    if not data:
        break
    print(f"Recieved Encrypted Data: {data}")
    key = int(input("Enter key to decrypt with (number): "))
    decrypted = decryptRailFence(data, key)
    print(f"Decrypted plain text: {decrypted}")

conn.close()
s.close()
```

### Railfence Client

```python
import socket

def encryptRailFence(text, key):
    rail = [['\n' for _ in range(len(text))] for _ in range(key)]
    dir_down = False
    row, col = 0, 0

    for i in range(len(text)):
        if row == 0 or row == key - 1:
            dir_down = not dir_down
        rail[row][col] = text[i]
        col += 1
        if dir_down:
            row = row + 1
        else:
            row = row - 1

    result = []
    for i in range(key):
        for j in range(len(text)):
            if rail[i][j] != '\n':
                result.append(rail[i][j])
    return "".join(result)


s = socket.socket()
s.connect(('127.0.0.1', 65432))

key = int(input("Enter the key to encrypt with (number): "))
text = input("Enter plain text to encrypt: ")

encrypted = encryptRailFence(text, key)
s.send(encrypted.encode())

s.close()
```

---

## 11. ADDITIONAL FILES

### us.py

```python
# playfair wala code yha likho  
```

### usc.py

```python

```

---

## SUMMARY

### Programs Included:
1. **TCP Server/Client** - Basic TCP socket communication
2. **UDP Server/Client** - Basic UDP socket communication
3. **CRC Server/Client** - Cyclic Redundancy Check for error detection
4. **Diffie-Hellman Server/Client** - Key exchange protocol
5. **Hamming Code Server/Client** - Error detection and correction
6. **LZW Server/Client** - Data compression algorithm
7. **Multichat Server/Client** - Multi-client chat application
8. **Odd/Even Server/Client** - Number classification service
9. **Playfair Cipher Server/Client** - Playfair encryption
10. **Railfence Cipher Server/Client** - Railfence encryption

### Port Numbers Used:
- TCP/UDP: 5000
- CRC: 6000
- Diffie-Hellman: 5001
- Hamming: 5000
- LZW: 65433
- Multichat: 5000
- Odd/Even: 5000
- Playfair: 60014
- Railfence: 65432

---

**Note:** Make sure to run server programs before starting their corresponding client programs. Some programs use the same port numbers, so run them separately to avoid conflicts.

