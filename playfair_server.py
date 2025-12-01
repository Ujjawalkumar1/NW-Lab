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