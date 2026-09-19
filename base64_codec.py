base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

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

plain_text = "Hello, Network Security! 2026"
encoded_text = encode(plain_text.encode('utf-8'))
decoded_text = decode(encoded_text).decode('utf-8')
print("原始明文：", plain_text)
print("编码结果：", encoded_text)
print("解码还原：", decoded_text)
