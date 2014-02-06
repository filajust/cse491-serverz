#!/usr/bin/env python
import random
import socket
import time
import urlparse
import cgi
#try:
    #from cStringIO import StringIO
#except:
from StringIO import StringIO

def extractPath(input):
    temp = input.splitlines()
    return temp[0].split(' ')[1]

# --------------------------------------------------------------------------------
#                                 Gets 
# --------------------------------------------------------------------------------

def index_html(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send("Content-type: text/html\r\n\r\n")

    contentUrl = '/content'
    fileUrl = '/file'
    imageUrl = '/image'
    formGetUrl = '/form'
    formPostUrl = '/formPost'
    formPostMultipartUrl = '/formPostMultipart'

    urls = '<h1>Hello, world.</h1>This is filajust\'s Web server.\r\n\r\n\
            <p><a href="{0}">Content</a></p>\
            <p><a href="{1}">File</a></p>\
            <p><a href="{2}">Image</a></p>\
            <p><a href="{3}">Form</a></p>\
            <p><a href="{4}">Form (post)</a></p>\
            <p><a href="{5}">Form (post multipart)</a></p>'.\
            format(contentUrl, fileUrl, imageUrl, formGetUrl, formPostUrl, 
                    formPostMultipartUrl)
    conn.send(urls);

def content_html(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send("Content-type: text/html\r\n\r\n")

    conn.send('<p>Content</p>')

def file_html(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send("Content-type: text/html\r\n\r\n")

    conn.send('<p>File</p>')

def image_html(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send("Content-type: text/html\r\n\r\n")

    conn.send('<p>Image</p>')

def form_html(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send("Content-type: text/html\r\n\r\n")

    conn.send('<p>Please fill in name</p>\
        <form action=\'/submit\' method=\'GET\'>\
        First Name: <input type=\'text\' name=\'firstname\'>\
        Last Name: <input type=\'text\' name=\'lastname\'>\
        <input type=\'submit\' value=\'Submit\'>\
        </form>')

def submit_html(data, conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send("Content-type: text/html\r\n\r\n")

    # get the query string, then use it as a parameter to get dictionary
    res = urlparse.parse_qs(urlparse.urlparse(data).query)
    if len(res) < 2: # check if the input was valid
        conn.send('<h1>Error</h1>')
    else:
        conn.send('<p>Hello Mr. {0} {1}</p>'.format(res\
                ['firstname'][0], res['lastname'][0]))

def urlencoded_html(form, conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send("Content-type: text/html\r\n\r\n")

    if "firstname" not in form or "lastname" not in form:
        conn.send('<h1>Input Error</h1>')
    else:
        # get the query string, then use it as a parameter to get dictionary 
        # (assumes it is of type application/x-www-form-urlencoded)
        firstname = form['firstname'].value
        lastname = form['lastname'].value
        if not firstname or not lastname: # check if the input was valid
            conn.send('<h1>Input Error</h1>')
        else:
            conn.send('<p>Hello Mr. {0} {1}, thank you for using a post \
                    request</p>'.format(firstname, lastname))

def multipart_html(form, conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send("Content-type: text/html\r\n\r\n")

    conn.send('<h1>multipart</h1>')
    print 'form: ', form['files'].value

def error_html(conn):
    conn.send('HTTP/1.0 404 Not Found\r\n');

    conn.send('<p>Error</p>')

    
def handle_get(path, conn):
    if path == '/':
        index_html(conn)
    elif path == '/content':
        content_html(conn)
    elif path == '/file':
        file_html(conn)
    elif path == '/image':
        image_html(conn)
    elif path == '/form':
        form_html(conn)
    elif path == '/formPost':
        form_post_html(conn)
    elif path == '/formPostMultipart':
        form_post_multipart_html(conn)
    elif path.startswith('/submit'):
        submit_html(path, conn)
    else:
        error_html(conn)

# --------------------------------------------------------------------------------
#                                  Posts
# --------------------------------------------------------------------------------

def form_post_html(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send("Content-type: text/html\r\n\r\n")

    conn.send('<p>Please fill in name</p>\
        <form action=\'/submit\' method=\'POST\' \
        enctype=\'application/x-www-form-urlencoded\'>\
        First Name: <input type=\'text\' name=\'firstname\'>\
        Last Name: <input type=\'text\' name=\'lastname\'>\
        <input type=\'submit\' value=\'Submit\'>\
        </form>')

def form_post_multipart_html(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send("Content-type: text/html\r\n\r\n")

    conn.send('<p>Please fill in name</p>\
        <form action=\'/submit\' method=\'POST\' \
        enctype=\'multipart/form-data\'>\
        File: <input type=\'file\' name=\'files\'>\
        <input type=\'submit\' value=\'Submit\'>\
        </form>')

def handle_post(headers, conn):

    '''
    headers = {}

    for x in range(0, 10):
        lineDict = buf.readline().split(' ')
        header = lineDict[0]
        data = ' '.join(lineDict[1:])
        headers[header] = data

    print 'headers: ', headers
    '''

    headers_dict = {}
    for line in headers:
        k, v = line.split(': ', 1)
        headers_dict[k.lower()] = v

    environ = {}
    environ['REQUEST_METHOD'] = 'POST'

    # credit to bjurgess1 on github
    content_length = headers_dict['content-length']
    content = conn.recv(int(content_length))

    form = cgi.FieldStorage(headers=headers_dict, fp=StringIO(content), environ=environ)

    print 'headers: ', headers_dict
    content_type = headers_dict['content-type']

    print 'content-type: ', content_type

    if 'application/x-www-form-urlencoded' in content_type:
        urlencoded_html(form, conn)
    elif 'multipart/form-data;' in content_type:
        multipart_html(form, conn)
    else:
        error_html(conn);

# --------------------------------------------------------------------------------
#                           handling the connection 
# --------------------------------------------------------------------------------
    
# Send response
# took some code from 
# http://stackoverflow.com/questions/8315209/sending-http-headers-with-python 
def handle_connection(conn):

        # credit to cameronkeif on github
        data = ''
        while data[-4:] != '\r\n\r\n':
            retVal = conn.recv(1)
            data = data + retVal

        print 'data: ', data

        '''
        1) the request line is always the first line ending with \r\n
        2) the header sentinel is '\r\n\r\n' -- that is, you need to read headers
           until you encounter that
        3) you need to pass the POST content on to cgi.FieldStorage without
           any interpretation or modification (no splitlines, etc.)
        '''

        requestType, theRest = data.split('\r\n', 1)
        headers_temp, content = theRest.split('\r\n\r\n', 1)

        headers = StringIO(headers_temp)
        # headers = data(StringIO(headers_temp))  

# print 'headers: ', headers.getvalue()

        if data:
            request = requestType.split(' ')[0]
            if request == 'POST':
                handle_post(headers, conn)
            elif request == 'GET':
                path = extractPath(data)
                handle_get(path, conn)

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

