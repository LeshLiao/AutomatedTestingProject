#!/usr/bin/env python3 
import socket 
import time

HOST = '127.0.0.1' 

PORT = 5050 

# set High Altitude to 1  # For Test
retBatchData = "FE CB 30 00 8E 00 00 00 02 00 8A 67 A2 67 7B 01 01 67 1A 01 00 67 36 01 00 67 7D 02 00 00 67 7C 02 00 00 67 7E 02 14 00 67 AF 01 00 67 4A 01 01 67 4D 01 03 67 4E 01 06 67 51 01 05 67 52 02 FF FF 67 53 02 0A 00 67 63 01 05 67 64 01 03 67 70 01 00 67 73 02 00 00 67 80 01 04 67 81 01 01 67 1B 01 00 67 42 01 00 67 4F 01 00 67 1F 01 00 67 43 01 00 67 44 01 13 67 75 01 00 67 76 02 01 00 67 0A 02 00 00 67 82 02 00 00 67 83 02 00 00 67 7E 02 14 00 0D"
retBatchData = retBatchData + "END"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
    print('listening...') 
    
    s.bind((HOST, PORT)) 
    s.listen() 
    conn, addr = s.accept() 
    with conn: 
        print('Connected by', addr) 
        while True: 
            #data = conn.recv(1024)
            
            data = conn.recv(1024).decode('ascii')
            
            print(f"[{addr}] {data}")
            
            if not data: 
                break 

            print("sleep")
            time.sleep(2)

            print("server send:"+retBatchData)
            conn.sendall(retBatchData.encode('ascii'))


