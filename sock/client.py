

import socket
import datetime
import json 

HOST = 'Alophants-Air.lan'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

# Create a socket object using socket.socket() method
# AF_INET is the address family of the socket. This is the Internet address family for IPv4.
# SOCK_STREAM is the socket type for TCP, the protocol that will be used to transport our messages in the network.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        
        message = input("Enter message: ")
        pack = {
            'type':'chat',
            'source':PORT,
            'message':message,
            'sent_time':str(datetime.datetime.now())
        }
        # override to send timestamp 
        # message = str(datetime.datetime.now())
        
        s.sendall( json.dumps( pack ).encode() )
        
        data = s.recv(1024)
        print(f'Received: {data.decode()}')



