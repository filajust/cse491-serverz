#!/usr/bin/env python
import random
import socket
import time
import urlparse

def extractPath(input):
    temp = input.splitlines()
    return temp[0].split(' ')[1]

def index_html():
    contentUrl = '/content'
    fileUrl = '/file'
    imageUrl = '/image'
    formGetUrl = '/form'
    formPostUrl = '/formPost'

    urls = '<h1>Hello, world.</h1>This is filajust\'s Web server.\r\n\r\n\
            <p><a href="{0}">Content</a></p>\
            <p><a href="{1}">File</a></p>\
            <p><a href="{2}">Image</a></p>\
            <p><a href="{3}">Form</a></p>\
            <p><a href="{4}">Form (post)</a></p>'.\
            format(contentUrl, fileUrl, imageUrl, formGetUrl, formPostUrl)
    return urls

def content_html():
    return '<p>Content</p>'

def file_html():
    return '<p>File</p>'

def image_html():
    return '<p>Image</p>'

def form_html():
    return '<p>Please fill in name</p>\
        <form action=\'/submit\' method=\'GET\'>\
        First Name: <input type=\'text\' name=\'firstname\'>\
        Last Name: <input type=\'text\' name=\'lastname\'>\
        <input type=\'submit\' value=\'Submit\'>\
        </form>'

def form_post_html():
    return '<p>Please fill in name</p>\
        <form action=\'/submit\' method=\'POST\' \
        enctype=\'application/x-www-form-urlencoded\'>\
        First Name: <input type=\'text\' name=\'firstname\'>\
        Last Name: <input type=\'text\' name=\'lastname\'>\
        <input type=\'submit\' value=\'Submit\'>\
        </form>'

def submit_html(data):
    # get the query string, then use it as a parameter to get dictionary
    res = urlparse.parse_qs(urlparse.urlparse(data).query)
    if len(res) < 2: # check if the input was valid
        return '<h1>Error</h1>'
    else:
        return '<p>Hello Mr. {0} {1}</p>'.format(res\
                ['firstname'][0], res['lastname'][0])

def error_html():
    return '<p>No Content</p>'
    
def handle_get(path):
    if path == '/':
        return index_html()
    elif path == '/content':
        return content_html()
    elif path == '/file':
        return file_html()
    elif path == '/image':
        return image_html()
    elif path == '/form':
        return form_html()
    elif path == '/formPost':
        return form_post_html()
    elif path.startswith('/submit'):
        return submit_html(path)
    else:
        return error_html()

def handle_post(data):
    if "firstname" not in data or "lastname" not in data:
        return '<h1>Error</h1>'
    else:
        # get the query string, then use it as a parameter to get dictionary 
        # (assumes it is of type application/x-www-form-urlencoded)
        temp = data.splitlines()
        res = urlparse.parse_qs(temp[-1])
        if len(res) < 2: # check if the input was valid
            return '<h1>Error</h1>'
        else:
            return '<p>Hello Mr. {0} {1}, thank you for using a post \
                    request</p>'.format(res['firstname'][0], res['lastname'][0])
    
# Send response
# took some code from 
# http://stackoverflow.com/questions/8315209/sending-http-headers-with-python 
def handle_connection(conn):
        conn.send('HTTP/1.0 200 OK\r\n')
        conn.send("Content-type: text/html\r\n\r\n")

        data = conn.recv(1000)

        if data:
            request = data.splitlines()[0].split(' ')[0]
            if request == 'POST':
                text = handle_post(data)
                conn.send(text)
            elif request == 'GET':
                path = extractPath(data)
                text = handle_get(path)
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

