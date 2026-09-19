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

plain_text = "Hello, Network Security! 2026"
cipher_text = b64encode(plain_text.encode('utf-8'))
decode_text = b64decode(cipher_text).decode('utf-8')
print("原始明文：", plain_text)
print("编码结果：", cipher_text)
print("解码还原：", decode_text)
