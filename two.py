import socket
import os
s=socket.socket(AF_INET,SOCK_STREAM)
s.connect('127.0.0.1',8888)
def sendfile(conn):
 str1 = conn.recv(1024)
 filename = str1.decode('utf-8')
 print('The client requests my file:',filename)
 if os.path.exists(filename):
 print('I have %s, begin to download!' % filename)
 s.send(b'yes')
s.recv(1024)
 size = 1024
 with open(filename,'rb') as f:
 while True:
 data = f.read(size)
s.send(data)
 if len(data) < size:
 break
 print('%s is downloaded successfully!' % filename)
 else:
 print('Sorry, I have no %s' % filename)
 s.send(b'no')
 s.close()
while True:
 (s,addr)=s.accept()
 sendfile(s)