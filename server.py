#!/usr/bin/env python
import random
import socket
import time

# Send response
# took some code from http://stackoverflow.com/questions/8315209/sending-http-headers-with-python 
def handle_connection(conn):
        conn.send('HTTP/1.0 200 OK\r\n')
        conn.send("Content-Type: text/html\r\n\r\n")
        conn.send('<html><body><h1>Hello World</h1> this is filajust\'s Web server</body></html>')
        conn.close()
    
def main():
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn() # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        
        print 'Got connection from', client_host, client_port
        handle_connection(c)
    
if __name__ == '__main__':
    main()

