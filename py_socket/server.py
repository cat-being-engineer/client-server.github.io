from socket import *
from time import ctime
from threading import Thread

Host= ''#表示可以使用任何可用的地址
PORT= 20000
BUFSIZ= 1024
ADDR = (Host, PORT)
tcpserver = socket(AF_INET,SOCK_STREAM)
tcpserver.bind(ADDR)
tcpserver.listen(5)

def usart():

 while True:
     print('wait for coneection')
     tcpclient,address = tcpserver.accept()
     
     print("%s %s" % ("connected from:",address))# %格式化字符串的方式
     while True:
         data = tcpclient.recv(BUFSIZ)
         if not data:
             break
         print( "%s" % (type(data)))
         tcpclient.send(data)

     tcpclient.close()


t1 = Thread(target=usart)

t2 = Thread(target=usart)

t1.start()
t2.start()

t1.join()
t2.join()

tcpserver.close()

