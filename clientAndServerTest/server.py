import socket 
import threading
import os
import time

HEADER = 64
PORT = 5050
#SERVER = socket.gethostbyname(socket.gethostname())    #real ip address
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)
#FORMAT = 'utf-8'
FORMAT = 'ascii'
DISCONNECT_MESSAGE = "!DISCONNECT"
SHUTDOWN_MESSAGE = "shutdown"
serverStatus = True

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        #if msg_length:
        if True:
            #msg_length = int(msg_length)
            msg = conn.recv(1024).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                
            if msg == SHUTDOWN_MESSAGE:
                print("os._exit(1)")
                conn.close()
                os._exit(1)
                
                
            print(f"[{addr}] {msg}")
            #print("sleep 1s")
            #time.sleep(1)
            conn.send("Msg received".encode(FORMAT))

    conn.close()
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while serverStatus:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()