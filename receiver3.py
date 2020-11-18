#!/usr/bin/python3

from socket import *

def handler(conn):
    c,addr = conn
    host,port = addr
    print(f'Connection accepted from {host} on port {port}')
    while 1:
        try:
            data = c.recv(1024).decode("utf-8").strip()
            if not data:
                break
            print(data)
        except:
            break
    print("Closing connection")
    c.close()

if __name__ == '__main__':
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    PORT = 5000
    s.bind(('127.0.0.1',PORT))
    s.listen(1)
    print(f'Line receiver listening on port {PORT}')
    while 1:
        try:
            conn = s.accept()
            handler(conn)
        except KeyboardInterrupt:
            print("[*] User interrupt")
            break


