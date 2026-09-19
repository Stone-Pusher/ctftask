import socket

host = '127.0.0.1'
port = 8888

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host, port))
server_socket.listen(1)
print("服务器启动，监听", host, ":", port)

conn, addr = server_socket.accept()
print("客户端已连接：", addr)

message = "Hello Client, this is Server!"
conn.sendall(message.encode('utf-8'))
print("服务器发送：", message)

data = conn.recv(1024)
print("服务器收到回复：", data.decode('utf-8'))

conn.close()
server_socket.close()
print("连接已关闭")
