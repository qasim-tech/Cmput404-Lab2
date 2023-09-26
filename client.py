#!/usr/bin/env python3

import socket, sys

def main():
    host = 'www.google.com'
    port = 80
    payload = 'GET / HTTP/1.0\r\nHost: ' + host + '\r\n\r\n'
    buffer_size = 4096
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except:
        print('Failed to create socket.')
        sys.exit()
    
    remote_ip = socket.gethostbyname(host)
    try:
        s.connect((remote_ip, port))
    except:
        print('Connection failed.')
        sys.exit()

    try:
        s.sendall(payload.encode())
    except:
        print('Send failed.')
        sys.exit()
    s.shutdown(socket.SHUT_WR)

    full_data = b''
    while True:
        data = s.recv(buffer_size)
        if not data:
            break
        full_data += data
    print(full_data)
    s.close()

if __name__ == '__main__':
    main()

