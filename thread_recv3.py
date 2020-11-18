#!/usr/bin/python3

from socket import *
import threading

def handler(conn):
    c,addr = conn
    host,port = addr
    print(f'Connection accepted from {host} on port {port}')
    print(f'Current thread: {threading.currentThread().name}')
    while 1:
        try:
            data = c.recv(1024).decode("utf-8").strip()
            if not data:
                break
            print(data)
        except:
            break
    print(f'Closing thread: {threading.currentThread().name}')
    c.close()

if __name__ == '__main__':
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    PORT = 5000
    s.bind(('0.0.0.0',PORT))
    s.listen(1)
    print(f'Line receiver listening on port {PORT}')
    while 1:
        try:
            conn = s.accept()
            t = threading.Thread(target=handler,args=(conn,)) 
            t.daemon = True
            t.start()
        except KeyboardInterrupt:
            print('[*] User interrupt')
            break


