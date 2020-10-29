import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 1338
max_connections = 5

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip,bind_port))
server.listen(max_connections)

print("[*] Listening on %s:%d, accepting max %d connections" %(bind_ip,bind_port,max_connections))

def handle_client(client_socket):
    request = client_socket.recv(1024)
    print("[*] Received the following request: %s" % request.decode())

    client_socket.send(b"ACK!")
    client_socket.close()

while True:
    client,addr = server.accept()
    print("[*] Received a new connection from: %s:%d" % (addr[0], addr[1]))
    print("[*] Starting a new thread for the client")
    client_thread = threading.Thread(target=handle_client,args=(client,))
    client_thread.start()