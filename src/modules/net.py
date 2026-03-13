import socket, sys, os, fcntl, errno, struct

PORT = 8080

def create_server():
    server_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_fd.bind(('', PORT))
    server_fd.listen(3)
    server_fd.setblocking(False)
    return server_fd

def connect_with(ip):
    client_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_fd.connect((ip, PORT))
    return client_fd

def accept_connections(server_fd):
    try:
        new_socket, _ = server_fd.accept()
        return new_socket
    except BlockingIOError:
        return -1

def send_message(new_socket, message):
    if new_socket != -1:
        new_socket.send(message.encode())

def get_message(new_socket):
    if new_socket != -1:
        return new_socket.recv(1024).decode()
    return None