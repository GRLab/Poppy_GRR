import httplib
import sys

server_address = ("192.168.0.158:4567") #adresse ip du serveur:port (changer l'IP en fonction)
server = httplib.HTTPConnection(server_address)

while 1:
	cmd = raw_input('input command (ex. set+robot+compliant):')
	#cmd = cmd.split()

	if cmd == 'exit' : #tipe exit to end
		break
	#request command to server
	server.request('POST', '?Submit='+cmd)

	#get response from server
	rsp = server.getresponse()

	#print server response and data
	print(rsp.status)

server.close()
