import socket
import json
import os

#using host=127.0.0.1 force server to work only on local environment
#host = '127.0.0.1'
#leaving in blank server will accept request from others on the same network
host = ''
port = 9100
main_directory = 'documentRoot'

def Main():
	#family AF_INET for IPV4 protocol TCP/UDP
	#connection type SOCK_STREAM for connection-oriented TCP byte stream
	mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#socket options: (socket-level, reutilice the socket and value 1 socket is known by this value)
	mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	#binding port to socket
	mySocket.bind(('127.0.0.1',port))
	#listen port socket 1
	mySocket.listen(1)
	#print server status
	if(mySocket):
		if(host == ''):
			print('Server running on local network port: '+str(port))
		else:
			print('Server running on '+host+' port: '+str(port))
	else:
		print('Oops! Im having issues setting the socket!')

	#persistent while loop
	while True:
		client_sock, client_addr = mySocket.accept()
		print('Connection from: '+ str(client_addr))
		request = client_sock.recv(1024).decode()
		#clean request string
		request = request.replace('\r\n\r\n','')
		request_data = request.split('\r\n')
		#stardarize
		if(request_data[0].split()[1].endswith('/')):
			requested_route = main_directory+request_data[0].split()[1]+'index.html'
		else:
			requested_route = main_directory+request_data[0].split()[1]

		##prepare response
		#data dictionary
		response = {
		'path': request_data[0].split()[1],
		'protocol': request_data[0].split()[2],
		'method': request_data[0].split()[0],
		}
		#headers dictionary
		pairs = {}
		iteration = iter(request_data)
		next(iteration)
		for item in iteration:
			item_split = item.split(' ',1)
			pairs[item_split[0].replace(':','')] = item_split[-1]
		#add headers dictionary
		response['headers'] = pairs
		json_data = json.dumps(response)
		#response to send
		response_text ='X-RequestEcho: '+json_data+'\r\n\r\n'

		if(os.path.exists(requested_route)):
			#correct path 127.0.0.1:9100/app1 (exists) to 127.0.0.1:9100/app1/index.html
			if not(requested_route.endswith('/')):
				if not(requested_route.endswith('.html')):
					requested_route = requested_route+'/index.html'
			
			#deliver status and data
			client_sock.sendall('HTTP/1.1 200 OK\r\n'.encode())
			client_sock.sendall(response_text.encode())

			#deliver html file
			file = open(requested_route,'r')
			for line in file:
				client_sock.sendall(line.encode())
			file.close()
		else:
			#deliver status and data
			client_sock.sendall('HTTP/1.1 404 Not Found\r\n'.encode())
			client_sock.sendall(response_text.encode())

		client_sock.close()
		print('Closed')

if __name__ == '__main__':
	Main()
