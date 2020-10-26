import socket

target_host = "127.0.0.1"
target_port = 80

#create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#connect the client and send some data
client.sendto(("GET / HTTP/1.1\r\nHost: %s\r\n\r\n" % target_host).encode("utf-8"), (target_host, target_port))

#receive data
response, adr = client.recvfrom(4096)
print(response.decode("utf-8"))welsch