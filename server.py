#!/usr/bin/env python
import random
import socket
import time
import urlparse
import cgi
import render
from StringIO import StringIO

# --------------------------------------------------------------------------------
#                                Functions 
# --------------------------------------------------------------------------------

def extractPath(input):
    temp = input.splitlines()
    return temp[0].split(' ')[1]

# --------------------------------------------------------------------------------
#                                 Gets 
# --------------------------------------------------------------------------------

def index_html(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send("Content-type: text/html\r\n\r\n")

    vars_dict = {'content_url': '/content', 'file_url': '/file', 
            'image_url': '/image', 'form_url': '/form', 'form_post_url': 'formPost',
            'form_post_multipart_url': 'formPostMultipart'}
    urls = render.render('index.html', vars_dict)

    conn.send(urls);

def content_html(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send("Content-type: text/html\r\n\r\n")

    html = render.render('content.html')
    conn.send(html)

def file_html(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send("Content-type: text/html\r\n\r\n")

    html = render.render('file.html')
    conn.send(html)

def image_html(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send("Content-type: text/html\r\n\r\n")

    html = render.render('image.html')
    conn.send(html)

def form_html(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send("Content-type: text/html\r\n\r\n")

    vars_dict = {'submit_url': '/submit'}

    html = render.render('form.html', vars_dict)
    conn.send(html)

def submit_html(data, conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send("Content-type: text/html\r\n\r\n")

    html = ''

    # get the query string, then use it as a parameter to get dictionary
    res = urlparse.parse_qs(urlparse.urlparse(data).query)
    if len(res) < 2: # check if the input was valid
        html = render.render('error.html')
    else:
        vars_dict = {'firstname': res['firstname'][0], 
            'lastname': res['lastname'][0]}
        html = render.render('submit.html', vars_dict)

    conn.send(html)

def urlencoded_html(form, conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send("Content-type: text/html\r\n\r\n")

    html = ''
    if "firstname" not in form or "lastname" not in form:
        html = render.render('error.html')
    else:
        # get the query string, then use it as a parameter to get dictionary 
        # (assumes it is of type application/x-www-form-urlencoded)
        firstname = form['firstname'].value
        lastname = form['lastname'].value
        if not firstname or not lastname: # check if the input was valid
            html = render.render('error.html')
        else:
            vars_dict = {'firstname': firstname, 'lastname': lastname}
            html = render.render('urlencoded.html', vars_dict)

    conn.send(html)

def multipart_html(form, conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send("Content-type: text/html\r\n\r\n")

    html = render.render('multipart.html')
    conn.send(html)
    # TODO: print 'form: ', form['files'].value

def send_404_html(conn):
    conn.send('404 Not Found')

def error_html(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send("Content-type: text/html\r\n\r\n")

    html = render.render('error.html')
    conn.send(html)
    
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
        send_404_html(conn)

# --------------------------------------------------------------------------------
#                                  Posts
# --------------------------------------------------------------------------------

def form_post_html(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send("Content-type: text/html\r\n\r\n")

    vars_dict = {'submit_url': '/submit'}

    html = render.render('form_post.html', vars_dict)
    conn.send(html)

def form_post_multipart_html(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send("Content-type: text/html\r\n\r\n")

    vars_dict = {'submit_url': '/submit'}

    html = render.render('form_post_multipart.html', vars_dict)
    conn.send(html)

def handle_post(headers, conn):
    headers_dict = {}
    for line in headers:
        k, v = line.split(': ', 1)
        headers_dict[k.lower()] = v

    environ = {}
    environ['REQUEST_METHOD'] = 'POST'

    # credit to bjurgess1 on github
    content_length = headers_dict['content-length']
    content = conn.recv(int(content_length))

    print 'content: ', content

    form = cgi.FieldStorage(headers=headers_dict, fp=StringIO(content), environ=environ)

    content_type = headers_dict['content-type']

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
        while '\r\n\r\n' not in data:
            retVal = conn.recv(10)
            data = data + retVal

        print 'data: ', data
        requestType, theRest = data.split('\r\n', 1)
        headers_temp, content = theRest.split('\r\n\r\n', 1)

        headers = StringIO(headers_temp)
        # headers = data(StringIO(headers_temp))  

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

