import socket

port = 12300
host = '46.214.127.51'

message_string = "I've connected!"
message_data = message_string.encode("utf-8")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.send(message_data)
s.close()