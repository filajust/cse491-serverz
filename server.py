#!/usr/bin/env python
import os
import sys
import random
import socket
import time
import urlparse
import cgi
import render
from StringIO import StringIO
from app import make_app

# --------------------------------------------------------------------------------
#                                Functions 
# --------------------------------------------------------------------------------

def extractPostData(conn, environ, headers_dict):
    content_length = headers_dict['content-length']
    data = conn.recv(int(content_length))
    environ['PATH_INFO'] = '/file'
    environ['CONTENT_LENGTH'] = content_length
    environ['QUERY_STRING'] = data
    environ['CONTENT_TYPE'] = headers_dict['content-type']
    environ['wsgi.input'] = StringIO(data)

def extractGetData(conn, environ, data):
    environ['PATH_INFO'] = extractPath(data)
    environ['CONTENT_LENGTH'] = 0
    environ['QUERY_STRING'] = ''
    environ['CONTENT_TYPE'] = 'text/html'

def extractPath(text):
    temp = text.splitlines()
    return temp[0].split(' ')[1]

# Send response
# took some code from 
# http://stackoverflow.com/questions/8315209/sending-http-headers-with-python 
def getEnvironData(conn):
    environ = {}

    # credit to cameronkeif on github
    data = ''
    while '\r\n\r\n' not in data:
        retVal = conn.recv(1)
        data = data + retVal

    requestType, theRest = data.split('\r\n', 1)
    headers_temp, content = theRest.split('\r\n\r\n', 1)

    headers_dict = {}
    headers = StringIO(headers_temp)

    for line in headers:
        if ':' in line:
            k, v = line.split(': ', 1)
            headers_dict[k.lower()] = v
        else:
            break

    request = requestType.split(' ')[0]
    environ['REQUEST_METHOD'] = request
    if request == 'POST':
        extractPostData(conn, environ, headers_dict)
    elif request == 'GET':
        extractGetData(conn, environ, data)

    return environ

# --------------------------------------------------------------------------------
#                           handling the connection 
# --------------------------------------------------------------------------------
    
# referenced bjurgess1 for solution
def handle_connection(conn):

    headers_set = []
    headers_sent = []

    def write(data):
        out = StringIO()
        if not headers_set:
            raise AssertionError("write() before start_response()")

        elif not headers_sent:
            # Before the first output, send the stored headers
            status, response_headers = headers_sent[:] = headers_set
            out.write('HTTP/1.0 %s\r\n' % status)
            for header in response_headers:
                out.write('%s: %s\r\n' % header)
            out.write('\r\n')

        out.write(data)
        conn.send(out.getvalue())

    def start_response(status, response_headers, exc_info=None):
        if exc_info:
            try:
                if headers_sent:
                    # Re-raise original exception if headers sent
                    raise exc_info[0], exc_info[1], exc_info[2]
            finally:
                exc_info = None     # avoid dangling circular ref
        elif headers_set:
            raise AssertionError("Headers already set!")

        headers_set[:] = [status, response_headers]
        return write


    the_wsgi_app = make_app()
    environ = getEnvironData(conn)
    result = the_wsgi_app(environ, start_response)

    try:
        if result:
            write(result)
        if not headers_sent:
            write('')
    finally:
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

