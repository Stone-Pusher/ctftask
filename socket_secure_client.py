import socket

host = '127.0.0.1'
port = 8889
shift = 5

def cipher(text, offset):
    result = ""
    for char in text:
        if char.islower():
            num = (ord(char) - ord('a') + offset) % 26
            result = result + chr(num + ord('a'))
        elif char.isupper():
            num = (ord(char) - ord('A') + offset) % 26
            result = result + chr(num + ord('A'))
        else:
            result = result + char
    return result

def getchar(num):
    if num < 26:
        return chr(num + ord('A'))
    elif num < 52:
        return chr(num - 26 + ord('a'))
    elif num < 62:
        return chr(num - 52 + ord('0'))
    elif num == 62:
        return '+'
    else:
        return '/'

def b64encode(data):
    result = ""
    i = 0
    length = len(data)
    while i < length:
        b1 = data[i]
        b2 = data[i+1] if i+1 < length else 0
        b3 = data[i+2] if i+2 < length else 0
        x1 = b1 >> 2
        x2 = ((b1 & 0x03) << 4) | (b2 >> 4)
        x3 = ((b2 & 0x0F) << 2) | (b3 >> 6)
        x4 = b3 & 0x3F
        result = result + getchar(x1)
        result = result + getchar(x2)
        result = result + (getchar(x3) if i+1 < length else '=')
        result = result + (getchar(x4) if i+2 < length else '=')
        i = i + 3
    return result

def getnum(char):
    if 'A' <= char <= 'Z':
        return ord(char) - ord('A')
    elif 'a' <= char <= 'z':
        return ord(char) - ord('a') + 26
    elif '0' <= char <= '9':
        return ord(char) - ord('0') + 52
    elif char == '+':
        return 62
    elif char == '/':
        return 63
    else:
        return 0

def b64decode(code):
    result = bytearray()
    i = 0
    while i < len(code):
        x1 = getnum(code[i])
        x2 = getnum(code[i + 1])
        x3 = getnum(code[i + 2])
        x4 = getnum(code[i + 3])
        if code[i + 2] == "=":
            x3 = 0
        if code[i + 3] == "=":
            x4 = 0
        y = (x1 << 18) + (x2 << 12) + (x3 << 6) + x4
        result.append((y >> 16) & 255)
        if code[i + 2] != "=":
            result.append((y >> 8) & 255)
        if code[i + 3] != "=":
            result.append(y & 255)
        i = i + 4
    return bytes(result)

def encode_encrypt(plain):
    step1 = b64encode(plain.encode('utf-8'))
    step2 = cipher(step1, shift)
    return step2

def decode_decrypt(cipher_text):
    step1 = cipher(cipher_text, -shift)
    step2 = b64decode(step1).decode('utf-8')
    return step2

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))
print("已连接到加密服务器", host, ":", port)

data = client_socket.recv(1024).decode('utf-8')
print("\n收到加密数据：", data)
decrypted = decode_decrypt(data)
print("解密后明文：", decrypted)

plain_text = "ok,已经收到信息"
print("\n回复明文：", plain_text)
encrypted = encode_encrypt(plain_text)
print("加密后发送：", encrypted)
client_socket.sendall(encrypted.encode('utf-8'))

client_socket.close()
print("\n连接已关闭")
