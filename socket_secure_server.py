import socket

host = '127.0.0.1'
port = 8889
shift = 5

base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

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

def encode(data):
    result = []
    i = 0
    length = len(data)
    while i < length:
        b0 = data[i]
        b1 = data[i+1] if i+1 < length else 0
        b2 = data[i+2] if i+2 < length else 0
        n0 = (b0 >> 2) & 0x3F
        n1 = ((b0 & 0x03) << 4) | ((b1 >> 4) & 0x0F)
        n2 = ((b1 & 0x0F) << 2) | ((b2 >> 6) & 0x03)
        n3 = b2 & 0x3F
        result.append(base64_chars[n0])
        result.append(base64_chars[n1])
        result.append(base64_chars[n2] if i+1 < length else '=')
        result.append(base64_chars[n3] if i+2 < length else '=')
        i += 3
    return ''.join(result)

def decode(s):
    s = s.rstrip('=')
    char_map = {c: i for i, c in enumerate(base64_chars)}
    result = bytearray()
    i = 0
    length = len(s)
    while i < length:
        v0 = char_map[s[i]]
        v1 = char_map[s[i+1]] if i+1 < length else 0
        v2 = char_map[s[i+2]] if i+2 < length else 0
        v3 = char_map[s[i+3]] if i+3 < length else 0
        result.append((v0 << 2) | (v1 >> 4))
        if i+2 < length:
            result.append(((v1 & 0x0F) << 4) | (v2 >> 2))
        if i+3 < length:
            result.append(((v2 & 0x03) << 6) | v3)
        i += 4
    return bytes(result)

def encode_encrypt(plain):
    step1 = encode(plain.encode('utf-8'))
    step2 = cipher(step1, shift)
    return step2

def decode_decrypt(cipher_text):
    step1 = cipher(cipher_text, -shift)
    step2 = decode(step1).decode('utf-8')
    return step2

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host, port))
server_socket.listen(1)
print("加密服务器启动，监听", host, ":", port)

conn, addr = server_socket.accept()
print("客户端已连接：", addr)

plain_text = "Hello Client! This is a secure message from Server."
print("\n原始明文：", plain_text)
encrypted = encode_encrypt(plain_text)
print("加密后发送：", encrypted)
conn.sendall(encrypted.encode('utf-8'))

data = conn.recv(1024).decode('utf-8')
print("\n收到加密数据：", data)
decrypted = decode_decrypt(data)
print("解密后明文：", decrypted)

conn.close()
server_socket.close()
print("\n连接已关闭")
