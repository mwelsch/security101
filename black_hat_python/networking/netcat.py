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
# upload = False
execute = ""
upload_destination = ""
target = "0.0.0.0"
port = 80
max_connections = 5


def parse_args():
    parser = argparse.ArgumentParser()
    define_args(parser)
    match_args_to_variables(parser)


def define_args(parser):
    parser.add_argument("-t", "--target", type=str, help="The ip address you want to target. Default is 0.0.0.0")
    parser.add_argument("-p", "--port", type=int,
                        help="The port of the target which should be targeted. Default is port 80")
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


def initialize_loops():
    global listen, port, target
    if listen:
        server_loop()
    elif port > 0 and len(target) > 0:
        print("Press CTRL+D if not sending input through stdin")
        buffer = sys.stdin.read()
        client_sender(buffer)


def client_sender(buffer):
    global target, port
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((target, port))

        if len(buffer):
            client.send(buffer.encode())
        while True:
            recv_len = 1
            response = ""
            while recv_len:
                data = client.recv(4096).decode()
                recv_len = len(data)
                response += data
                if recv_len < 4096:
                    break
            print(response)
            buffer = input("")
            buffer += "\n"
            client.send(buffer.encode())
    except Exception as e:
        print("[*] Exception. Exiting")
        print("[*] Exception: %s" % e)
        client.close()


def server_loop():
    global target
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)

    while True:
        clien_socket, addr = server.accept()
        client_thread = threading.Thread(target=client_handler, args=(clien_socket,))
        client_thread.start()


def client_handler(client_socket):
    global execute, command, upload_destination

    if len(upload_destination):
        file_buffer = ""
        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data
            client_socket.send(write_file(upload_destination, file_buffer))

    if len(execute):
        output = run_command(execute)
        client_socket.send(output)

    if command:
        command_shell(client_socket)


def write_file(destination, file_buffer):
    try:
        file_descriptor = open(upload_destination, "wb")
        file_descriptor.write(file_buffer)
        file_descriptor.close()
        output = "[*] Successfully saved file to %s\r\n" % upload_destination
    except:
        output = "[*] Failed to save file to %s\r\n" % upload_destination
    return output


def run_command(command):
    command = command.rstrip()
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "[*] Failed to execute command. Exiting"
    return output


def command_shell(client_socket):
    while True:
        client_socket.send(b"<netcat:#> ")
        cmd_buffer = ""
        while "\n" not in cmd_buffer:
            cmd_buffer += client_socket.recv(1024).decode()
        response = run_command(cmd_buffer)
        if type(response) is not bytes:
            response = response.encode()
        client_socket.send(response)


if __name__ == "__main__":
    parse_args()
    initialize_loops()
