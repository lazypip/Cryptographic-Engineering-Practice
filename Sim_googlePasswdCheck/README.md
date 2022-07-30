# Google password check scheme

## Description

​	google拥有泄露的密码库（包含'123456' - '12345678'作为测试），并按签名将其分成不同group。用户发送待检测信息的签名值，Server返回这一签名值所在的Group。用户若发现签名值在此Group出现，则密钥泄露。

```bash
# 代码可直接运行
python server.py  # listen
python client.py  # send
```

## API

Client

```python
# 待检测数据
username = "123456"
passwd = "12345678"
data = username + passwd
a = 0x77  # 测试私钥

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind(('127.0.0.1', 7777))
server_addr = ('127.0.0.1', 8888)
# [passwd check API]
generateSig(data, a, client_socket, ('127.0.0.1', 8888))
check(a, client_socket)
```

Server

```python
b = 0xf7  # 简化私钥
# 建立模拟密码库
dataList = generateDict(b)
server_addr = ('127.0.0.1', 8888)

# [Server API - listen消息并计算回送]
while True:
    reply(b, dataList, server_addr)
    print("check one")
```

## Demo

client测试'123456' - '12345678'是否在泄露数据库中（在现实场景中仅发送hash - 61648，此处仅做展示）

![image-20220730134924800](https://raw.githubusercontent.com/lazypip/readme_pices/main/crypto_pic/image-20220730134924800.png)