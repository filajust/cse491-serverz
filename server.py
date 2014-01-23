#!/usr/bin/env python
import random
import socket
import time

def extractPath(input):
    temp = input.splitlines()
    temp2 = temp[0].split(' ')
    return temp2[1]

def extractUrl(input):
    temp = input.splitlines()
    temp2 = temp[1].split(' ')
    return temp2[1]

def isPost(input):
    temp = input.splitlines()
    temp2 = temp[0].split(' ')[0]
    if temp2 == 'POST':
        return True
    else:
        return False
    
def HTMLContentFromPath(path, url):
    if path == '/':
        contentUrl = 'http://' + url + '/content'
        fileUrl = 'http://' + url + '/file'
        imageUrl = 'http://' + url + '/image'

        url = '<p><a href="' + \
                contentUrl + '">' + contentUrl + '</a></p><p><a href="' + \
                fileUrl + '">' + fileUrl + '</a></p><p><a href="' + \
                imageUrl + '">' + imageUrl + \
                '</a></p>'
        return url
    elif path == '/content':
        return '<p>content</p>'
    elif path == '/file':
        return '<p>file</p>'
    elif path == '/image':
        return '<p>image</p>'
    else:
        return '<p>no content</p>'
    
# Send response
# took some code from 
# http://stackoverflow.com/questions/8315209/sending-http-headers-with-python 
def handle_connection(conn):
        conn.send('HTTP/1.0 200 OK\r\n')
        conn.send("Content-type: text/html\r\n\r\n")
        conn.send('<h1>Hello, world.</h1>This is filajust\'s Web server.\r\n\r\n')

#data = '';
#while len(data) < 1000:
#chunk = conn.recv(100-len(data))
#if chunk == '':
#raise RuntimeError("socket connection broken")
#data = data + chunk

        data = conn.recv(1000)

        if data:
            if isPost(data):
                print 'That was a post request\n'
            else:
                path = extractPath(data)
                url = extractUrl(data)

                text = HTMLContentFromPath(path, url)
                if text:
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

