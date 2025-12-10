
import socket
import logging
from datetime import datetime
from pathlib import Path

Path('logs').mkdir(exist_ok=True)
#### for log ####
access_logger = logging.getLogger("access")
access_logger.setLevel(logging.INFO)
access_logger.propagate = False  

access_handler = logging.FileHandler("logs/web_server.log")
access_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
access_handler.setFormatter(formatter)
access_logger.addHandler(access_handler)

error_logger = logging.getLogger("errors")
error_logger.setLevel(logging.ERROR)
error_logger.propagate = False  

error_handler = logging.FileHandler("logs/error.log")
error_handler.setLevel(logging.ERROR)
error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
error_handler.setFormatter(error_formatter)
error_logger.addHandler(error_handler)

def log_access(addr, method, path, status, agent):
    now = datetime.now().strftime("%d/%b/%Y:%H:%M:%S")
    log_line = f'{addr} - - [{now}] "{method} {path} HTTP/1.1" {status}  "{agent}"'
    access_logger.info(log_line)  
########

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 80

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))

server_socket.listen(5)
print(f"server is listening on port {SERVER_PORT}... ")

while True:
    connection_socket, client_add = server_socket.accept()
    
    try:
        request = connection_socket.recv(1024).decode()
        
        if not request:
            connection_socket.close()
            continue
        
        status = 500
        method = "UNKNOWN"
        path = "UNKNOWN"
        agent = "unknown"
        response = b""
        
        for line in request.split('\n'):
            if line.lower().startswith('user-agent:'):
                agent = line.split(':', 1)[1].strip()
                break
        
        header = request.split('\n')[0]
        parts = header.split()
        
        if len(parts) < 2:
            status = 400
            response = b"HTTP/1.1 400 Bad Request\r\n\r\nMalformed Request"
            connection_socket.send(response)
            error_logger.error(f"Malformed request from {client_add}: {header}")
            log_access(client_add, "UNKNOWN", "UNKNOWN", status, agent)
            connection_socket.close()
            continue
        
        method, path = parts[0], parts[1]
        
        if path == '/':
            if method == "GET":
                try:
                    with open('static/index.html', 'rb') as f:
                        file = f.read()
                    status = 200
                    response = b"HTTP/1.1 200 OK\r\n\r\n" + file
                except FileNotFoundError:
                    status = 404
                    response = b"HTTP/1.1 404 Not Found\r\n\r\nFile Not Found"
                    error_logger.error(f"Missing file requested: {client_add} -> {path}")
            else:
                status = 405
                response = b"HTTP/1.1 405 Method Not Allowed\r\n\r\n"
        
        else:
            file_address = 'static' + path
            if method == "GET":
                try:
                    with open(file_address, 'rb') as f:
                        file = f.read()
                    status = 200
                    response = b"HTTP/1.1 200 OK\r\n\r\n" + file
                except FileNotFoundError:
                    status = 404
                    response = b"HTTP/1.1 404 Not Found\r\n\r\nFile Not Found"
                    error_logger.error(f"Missing file requested: {client_add} -> {path}")
            else:
                status = 405
                response = b"HTTP/1.1 405 Method Not Allowed\r\n\r\n"
        
        try:
            connection_socket.send(response)
            log_access(client_add, method, path, status, agent)
        except Exception as e:
            error_logger.exception(f"Failed sending response to {client_add}")
        
    except Exception as e:
        status = 500
        response = b"HTTP/1.1 500 Internal Server Error\r\n\r\nServer Error"
        error_logger.exception(f"Crash handling request from {client_add}")
        try:
            connection_socket.send(response)
            log_access(client_add, method, path, status, agent)
        except Exception:
            error_logger.exception(f"Failed sending response to {client_add}")
    
    finally:
        connection_socket.close()