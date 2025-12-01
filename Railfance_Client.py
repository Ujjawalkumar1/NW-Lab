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
