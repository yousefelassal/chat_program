import socket
import threading

HEADER = 1024	

#Using unused port to run server
PORT = 5050

# Gets IPv4 adress of the host computer automatically
SERVER = socket.gethostbyname(socket.gethostname())

ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
clients = []
def handle_client(conn, addr):
	'''handles new connections to the server '''
	print(f"[NEW CONNECTION] {addr} connected.")
	#display when a new user is connected
	broadcastMessage("new user has joined the room!".encode(FORMAT))
	connected = True
	while connected:
		message = conn.recv(HEADER)
		broadcastMessage(message)

	conn.close()    


def start():
	'''accept new connections to the server and print number of active connections '''
	server.listen()
	print(f"server is listening on {SERVER}")
	while True:
		conn, addr = server.accept()
		clients.append(conn)
		thread = threading.Thread(target=handle_client, args=(conn, addr))
		thread.start()
		print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

def broadcastMessage(message): 
	'''display messages to all users in the server '''
	for client in clients:
		client.send(message)
        
print("[STARTING] server is starting...")
start()




