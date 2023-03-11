#!usr/bin/env python3
from socket import *
from time import ctime

Host = 'DESKTOP-8HV7R6O'
PORT = 20000
BUFSIZ = 1024
ADDR = (Host,PORT)

tcpclient = socket(AF_INET,SOCK_STREAM)
tcpclient.connect(ADDR)

while True:
    data = input('输入数据')
    print("数据类型为%s" % (type(data)))
    if not data:
        break
    tcpclient.send(data.encode())
    data = tcpclient.recv(BUFSIZ)
    if not data:
        break
    print(data)
tcpclient.close()

