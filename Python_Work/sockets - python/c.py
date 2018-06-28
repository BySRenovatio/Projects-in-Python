__author__ = 'BYSorynyos'
import socket
server = "46.214.127.51"
port = 1337
sock = socket.socket()
sock.connect((server, port))
print "connected"
