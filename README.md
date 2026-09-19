# 网络编程 + 密码学 实验代码

本实验完成了 4 个任务，全部使用 **Python** 实现。

---

## 任务清单

| 任务 | 说明 |
|------|------|
| 任务1 | 古典密码（凯撒密码）的加密解密 |
| 任务2 | 编码算法（Base64）的编码解码 |
| 任务3 | 基础 TCP Socket 通信：server 发消息，client 回复 |
| 任务4 | 完整加密通信：发送先编码再加密，接收先解码再解密 |

---

## 文件列表

| 文件名 | 对应任务 | 运行方式 |
|--------|----------|----------|
| `caesar_cipher.py` | 任务1：凯撒密码 | `python caesar_cipher.py` |
| `base64_codec.py` | 任务2：Base64 编码 | `python base64_codec.py` |
| `socket_basic_server.py` | 任务3：基础服务器 | `python socket_basic_server.py` |
| `socket_basic_client.py` | 任务3：基础客户端 | `python socket_basic_client.py` |
| `socket_secure_server.py` | 任务4：加密服务器 | `python socket_secure_server.py` |
| `socket_secure_client.py` | 任务4：加密客户端 | `python socket_secure_client.py` |

---

## 使用方法

### 任务1 & 任务2（单独测试）

直接运行即可，会自动演示加密/编码 → 解密/解码 的完整流程并验证正确性。

### 任务3 & 任务4（Socket 通信）

需要**先启动服务器，再启动客户端**：

```bash
# 终端1：启动服务器
python socket_basic_server.py

# 终端2：启动客户端
python socket_basic_client.py
```

加密通信同理，把文件名换成 `socket_secure_server.py` / `socket_secure_client.py` 即可。

---

## 核心知识点

### 1. 凯撒密码（古典密码）
- 原理：明文字母按字母表顺序偏移固定位数（密钥）
- 特点：对称加密，加密解密用同一个密钥
- 局限性：密钥空间只有 25 种，极易被暴力破解

### 2. Base64 编码
- 原理：将 3 字节二进制数据拆成 4 个 6 位组，映射到 64 个可打印字符
- 注意：Base64 是**编码**不是加密，任何人都可以解码
- 用途：在文本协议中传输二进制数据

### 3. TCP Socket 通信流程

**服务器端：**
```
socket() → bind() → listen() → accept() → recv()/send() → close()
```

**客户端：**
```
socket() → connect() → recv()/send() → close()
```

### 4. 完整加密通信流程

**发送方：**
```
明文 → Base64编码 → 凯撒加密 → 网络发送
```

**接收方：**
```
网络接收 → 凯撒解密 → Base64解码 → 明文
```

---

## C/S 与 B/S 架构区别

| 对比项 | C/S 架构 | B/S 架构 |
|--------|----------|----------|
| 全称 | Client/Server（客户端-服务器） | Browser/Server（浏览器-服务器） |
| 客户端 | 需要安装专用客户端软件 | 只需浏览器 |
| 升级维护 | 客户端服务器都要升级 | 只需升级服务器 |
| 响应速度 | 快（本地有处理能力） | 相对慢（依赖网络） |
| 安全性 | 较高（专用客户端） | 较低（暴露在公网） |
| 典型例子 | QQ、微信桌面版 | 网页版邮箱、在线文档 |

---

## 验证结果

所有程序均已测试通过：
- ✅ 凯撒密码：加解密结果正确
- ✅ Base64 编码：与标准库结果一致
- ✅ 基础 Socket：通信正常
- ✅ 加密 Socket：加解密后数据一致
