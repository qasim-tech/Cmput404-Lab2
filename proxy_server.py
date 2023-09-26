#!/usr/bin/env python3

import socket, time
import threading

BYTES_TO_READ = 4096
PROXY_HOST = ''
PROXY_PORT = 8080
REMOTE_HOST = 'www.google.com'
REMOTE_PORT = 80

def handle_request(conn, addr):
    with conn:
        full_data = b''
        while True:
            data = conn.recv(BYTES_TO_READ)
            if not data:
                break
            full_data += data

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
            remote_ip = socket.gethostbyname(REMOTE_HOST)
            proxy_end.connect((remote_ip, REMOTE_PORT))

            print(f'Sending received data {full_data} to google')
            proxy_end.send(full_data)
            proxy_end.shutdown(socket.SHUT_WR)
            
            response_data = b''
            while True:
                data = proxy_end.recv(BYTES_TO_READ)
                if not data:
                    break
                response_data += data
        print(f'Sending received data {response_data} to client')
        conn.sendall(response_data)
        conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        server_socket.bind((PROXY_HOST, PROXY_PORT))
        server_socket.listen(2)
        
        while True:
            conn, addr = server_socket.accept()
            print('Connected by', addr)
            thread = threading.Thread(target=handle_request, args=(conn, addr))
            thread.run()
    

if __name__ == '__main__':
    main()