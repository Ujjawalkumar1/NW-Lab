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
