#!/usr/bin/env python3

import socket, time, threading

HOST = ''
PORT = 8001
BUFFER_SIZE = 1024

def handle_echo(conn, addr):
    with conn:
        full_data = conn.recv(BUFFER_SIZE)
        time.sleep(0.5)
        conn.sendall(full_data)
        conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        s.bind((HOST, PORT))
        s.listen(2)
        
        while True:
            conn, addr = s.accept()
            print('Connected by', addr)
            thread = threading.Thread(target=handle_echo, args=(conn, addr))
            thread.run()


if __name__ == '__main__':
    main()