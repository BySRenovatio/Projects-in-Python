__author__ = 'BYSorynyos'
#server
import socket
myip = socket.gethostbyname(socket.gethostname())
port = 1338
sock = socket.socket()
sock.bind((myip, port))
sock.listen(5)
print sock.accept()[1]