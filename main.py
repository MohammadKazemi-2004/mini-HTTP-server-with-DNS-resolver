import socket
import logging
from datetime import datetime


logging.basicConfig(
    filename="logs/web_server.log",
    level=logging.INFO,
    format='%(message)s'
)
def log_access(addr, method, path, status, agent):
    now = datetime.now().strftime("%d/%b/%Y:%H:%M:%S")

    log_line = f'{addr} - - [{now}] "{method} {path} HTTP/1.1" {status}  "{agent}"'
    logging.info(log_line)




SERVER_HOST = '127.0.0.1'
SERVER_PORT = 80

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # ipv4 - tcp
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # changing some default behavior
server_socket.bind((SERVER_HOST, SERVER_PORT))

server_socket.listen(5)
print(f"server is listening on port {SERVER_PORT}... ")

while True:
    connection_socket, client_add = server_socket.accept()
    print(f"client_add = {client_add}")
    request = connection_socket.recv(1024).decode()
    agent = 'unknown'
    for line in request.split('\n'):
        if line.lower().startswith('user-agent:'):
            agent = line.split(':',1)[1].strip()
    header = request.split('\n')[0]
    
    # for empty requests 
    if not request:
        connection_socket.close()
        continue
    
    method, path, _ = header.split()

    print(f'agent = {agent}')
        
    status=404
    if path == '/':
        if method == "GET":
            with open('static/index.html', 'rb') as f:
                file = f.read()
            status = 200
            response = b"HTTP/1.1 200 OK\n\n" + file
        else:
            status = 405
            response = b"HTTP/1.1 405 Methon Not Allowed\n\n"
              
    elif path == '/style.css':
        if method == "GET":
            with open('static/style.css', 'rb') as f:
                file = f.read()
            status = 200
            response = b"HTTP/1.1 200 OK\n\n" + file
        else:
            status = 405
            response = b"HTTP/1.1 405 Methon Not Allowed\n\n"
            
    elif path == '/script.js':
        if method == "GET":
            with open('static/script.js', 'rb') as f:
                file = f.read()
            status = 200
            response = b"HTTP/1.1 200 OK\n\n" + file
        else:
            status = 405
            response = b"HTTP/1.1 405 Methon Not Allowed\n\n"
                
    elif path == '/images/logo.png':
        if method == "GET":
            with open('static/images/logo.png', 'rb') as f:
                file = f.read()
            status = 200
            response = b"HTTP/1.1 200 OK\n\n" + file
        else:
            status = 405
            response = b"HTTP/1.1 405 Methon Not Allowed\n\n"
        
    elif path == '/global-network.png':
        if method == "GET":
            with open('static/images/global-network.png', 'rb') as f:
                file = f.read()
            status = 200
            response = b"HTTP/1.1 200 OK\n\n" + file
    else:
        status = 405
        response = b"HTTP/1.1 405 Methon Not Allowed\n\n"
                

        
    connection_socket.send(response)
    connection_socket.close()
        
        
    log_access(client_add, method, path, status, agent)
        
        
        
