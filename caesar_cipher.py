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

plain_text = "Hello, Network Security! 2026"
shift = 3

cipher_text = cipher(plain_text, shift)
decode_text = cipher(cipher_text, -shift)
print("原始明文：", plain_text)
print("加密密文：", cipher_text)
print("解密还原：", decode_text)
