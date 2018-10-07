import socket

ipaddr = "192.168.254.105"
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect ((ipaddr, 6969))
sock.sendall("Hello Master")
data = sock.recv(4096)
print (data)

#sock.close()


