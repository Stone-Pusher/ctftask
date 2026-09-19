import socket

host = '127.0.0.1'
port = 8888

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))
print("已连接到服务器", host, ":", port)

data = client_socket.recv(1024)
print("客户端收到：", data.decode('utf-8'))

reply = "ok,已经收到信息"
client_socket.sendall(reply.encode('utf-8'))
print("客户端回复：", reply)

client_socket.close()
print("连接已关闭")
