"""
A replacement for the common Linux command netcat, writtn in python
"""
import sys
import socket
import threading
import subprocess
import argparse

listen = False
command = False
upload = False
execute = ""
upload_destination = ""
target = "127.0.0.1"
port = 0


def parse_args():
    parser = argparse.ArgumentParser()
    define_args(parser)
    match_args_to_variables(parser)


def define_args(parser):
    parser.add_argument("-t", "--target", type=str, help="The ip address you want to target")
    parser.add_argument("-p", "--port", type=int, help="The port of the target which should be targeted")
    parser.add_argument("-l", "--listen", action="store_true", help="If used,"
                                                                    "listen for incoming connections on [target]:[port]")
    parser.add_argument("-e", "--execute", type=str, help="Execute the given file/command upon receiving a connection."
                                                          "Provide absolute path if possible")
    parser.add_argument("-c", "--command", action="store_true", help="If used a command shell will be initialized")
    parser.add_argument("-u", "--upload", type=str, help="Upon receiving connection upload a file"
                                                         "to the given destination")


def match_args_to_variables(parser):
    global target, port, execute, upload_destination, listen, command
    args = parser.parse_args()
    if args.target is not None:
        target = args.target
    if args.port is not None:
        port = args.port
    if args.execute is not None:
        execute = args.execute
    if args.upload is not None:
        upload_destination = args.upload
    listen = args.listen
    command = args.command



def initsmth():
    global listen,port,target
    if listen:
        server_loop()
    elif port > 0 and len(target)>0:
        print("Press CTRL+D if not sending input through stdin")
        buffer = sys.stdin.read()
        client_sender(buffer)


def client_sender(buffer):
    global target,port
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((target,port))

        if len(buffer):
            client.send(buffer)
            while True:
                recv_len = 1
                response = ""
                while recv_len:
                    data = client.recv(4096)
                    recv_len = len(data)
                    response += data
                    if recv_len < 4096:
                        break
                print(response)
                buffer = input("")
                buffer += "\n"

                client.send(buffer)
    except:
        print("[*] Exception. Exiting")
        client.close()


def server_loop():
    pass


if __name__ == "__main__":
    parse_args()
