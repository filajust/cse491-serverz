#!/usr/bin/env python
import random
import socket
import time

def extractPath(input):
    temp = input.splitlines()
    return temp[0].split(' ')[1]
    
def HTMLContentFromPath(path):
    if path == '/':
        contentUrl = '/content'
        fileUrl = '/file'
        imageUrl = '/image'

        urls = '<p><a href="' + \
                contentUrl + '">' + 'Content' + '</a></p><p><a href="' + \
                fileUrl + '">' + 'File' + '</a></p><p><a href="' + \
                imageUrl + '">' + 'Image' + \
                '</a></p>'
        return urls
    elif path == '/content':
        return '<p>Content</p>'
    elif path == '/file':
        return '<p>File</p>'
    elif path == '/image':
        return '<p>Image</p>'
    else:
        return '<p>No Content</p>'
    
# Send response
# took some code from 
# http://stackoverflow.com/questions/8315209/sending-http-headers-with-python 
def handle_connection(conn):
        conn.send('HTTP/1.0 200 OK\r\n')
        conn.send("Content-type: text/html\r\n\r\n")
        conn.send('<h1>Hello, world.</h1>This is filajust\'s Web server.\r\n\r\n')

        data = conn.recv(1000)

        if data:
            request = data.splitlines()[0].split(' ')[0]
            if request == 'POST':
                print 'That was a post request\n'
            elif request == 'GET':
                path = extractPath(data)
                text = HTMLContentFromPath(path)
                conn.send(text)

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

