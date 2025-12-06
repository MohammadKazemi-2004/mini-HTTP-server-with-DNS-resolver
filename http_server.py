# import socket
# import logging
# from datetime import datetime

# logging.basicConfig(
#     filename="logs/web_server.log",
#     level=logging.INFO,
#     format='%(message)s'
# )

# error_logger = logging.getLogger("errors")
# fh = logging.FileHandler("logs/error.log")
# fh.setLevel(logging.ERROR)
# error_logger.addHandler(fh)

# def log_access(addr, method, path, status, agent):
#     now = datetime.now().strftime("%d/%b/%Y:%H:%M:%S")

#     log_line = f'{addr} - - [{now}] "{method} {path} HTTP/1.1" {status}  "{agent}"'
#     logging.info(log_line)




# SERVER_HOST = '127.0.0.1'
# SERVER_PORT = 80

# server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # ipv4 - tcp
# server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # changing some default behavior
# server_socket.bind((SERVER_HOST, SERVER_PORT))

# server_socket.listen(5)
# print(f"server is listening on port {SERVER_PORT}... ")

# while True:
#     response = b""        
#     status = 500           #(default internal error)
#     method = "UNKNOWN"    
#     path = "UNKNOWN"      
#     agent = "unknown"
    
#     connection_socket, client_add = server_socket.accept()
#     # print(f"client_add = {client_add}")
#     try:
#         request = connection_socket.recv(1024).decode()
#         for line in request.split('\n'):
#             if line.lower().startswith('user-agent:'):
#                 agent = line.split(':',1)[1].strip()
#                 break
        
#         # for empty requests 
#         if not request:
#             connection_socket.close()
#             continue
        
#         header = request.split('\n')[0]
#         parts = header.split()
        
#         if len(parts) < 2 :
#             error_logger.error(f"Malformed request from {client_add}: {header}")
#             status = 400
#             response = b"HTTP/1.1 400 Bad Request\r\n\r\nMalformed Request"
#             connection_socket.send(response)
#             connection_socket.close()
#             continue
        
#         method, path = parts[0], parts[1]
            
#         status=404
#         if path == '/':
#             if method == "GET":
#                 with open('static/index.html', 'rb') as f:
#                     file = f.read()
#                 status = 200
#                 response = b"HTTP/1.1 200 OK\n\n" + file
#             else:
#                 status = 405
#                 response = b"HTTP/1.1 405 Methon Not Allowed\n\n"
        
#         else :
#             file_address = 'static' + path     
#             if method == "GET":
#                 with open(file_address, 'rb') as f:
#                     file = f.read()
#                 status = 200
#                 response = b"HTTP/1.1 200 OK\n\n" + file
#             else:
#                 status = 405
#                 response = b"HTTP/1.1 405 Methon Not Allowed\n\n"       

#             try:
#                 connection_socket.send(response)
#             except Exception:
#                 error_logger.exception(f"Failed sending response to {client_add}")


#         if status < 400:     # <-- فقط لاگ برای 2xx و 3xx و 405
#             log_access(client_add, method, path, status, agent)
#     except FileNotFoundError:
#         status = 404
#         response = b"HTTP/1.1 404 Not Found\r\n\r\nFile Not Found"
#         error_logger.error(f"{client_add} requested missing file: {path}") 
#         try:
#             connection_socket.send(response)
#         except Exception:
#             error_logger.exception(f"Failed sending response to {client_add}")
        
#     except Exception as e:
#         status = 500
#         response = b"HTTP/1.1 500 Internal Server Error\r\n\r\nServer Error"
#         error_logger.exception(f"Crash handling request from {client_add}")
#         try:
#             connection_socket.send(response)
#         except Exception:
#             error_logger.exception(f"Failed sending response to {client_add}")
    
#     finally:
#         connection_socket.close()
        
        

import socket
import logging
from datetime import datetime

# تنظیمات لاگر اصلی برای دسترسی‌ها
access_logger = logging.getLogger("access")
access_logger.setLevel(logging.INFO)
access_logger.propagate = False  # جلوگیری از انتشار به روت لاگر

access_handler = logging.FileHandler("logs/web_server.log")
access_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
access_handler.setFormatter(formatter)
access_logger.addHandler(access_handler)

# تنظیمات لاگر برای خطاها
error_logger = logging.getLogger("errors")
error_logger.setLevel(logging.ERROR)
error_logger.propagate = False  # جلوگیری از انتشار به روت لاگر

error_handler = logging.FileHandler("logs/error.log")
error_handler.setLevel(logging.ERROR)
error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
error_handler.setFormatter(error_formatter)
error_logger.addHandler(error_handler)

def log_access(addr, method, path, status, agent):
    now = datetime.now().strftime("%d/%b/%Y:%H:%M:%S")
    log_line = f'{addr} - - [{now}] "{method} {path} HTTP/1.1" {status}  "{agent}"'
    access_logger.info(log_line)  # استفاده از access_logger به جای logging

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
        
        # برای درخواست‌های خالی
        if not request:
            connection_socket.close()
            continue
        
        # مقداردهی اولیه متغیرها
        status = 500
        method = "UNKNOWN"
        path = "UNKNOWN"
        agent = "unknown"
        response = b""
        
        # استخراج user-agent
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
        
        # ارسال پاسخ
        try:
            connection_socket.send(response)
            # لاگ کردن دسترسی (همه وضعیت‌ها)
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