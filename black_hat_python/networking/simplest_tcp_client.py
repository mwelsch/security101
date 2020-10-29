import socket

target_host = "127.0.0.1"
target_port = 1338

#create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connect the client
client.connect((target_host, target_port))

#send some data
client.send(("GET / HTTP/1.1\r\nHost: %s\r\n\r\n" % target_host).encode("utf-8"))

#receive data
response = client.recv(4096)
print(response.decode("utf-8"))