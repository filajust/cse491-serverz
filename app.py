#!/usr/bin/env python
import random
import socket
import time
import urlparse
import cgi
import render
from StringIO import StringIO
from wsgiref.util import setup_testing_defaults

# --------------------------------------------------------------------------------
#                                 Gets 
# --------------------------------------------------------------------------------

def index_html():
    vars_dict = {'content_url': '/content', 'file_url': '/file', 
            'image_url': '/image', 'form_url': '/form', 'form_post_url': '/formPost',
            'form_post_multipart_url': '/formPostMultipart'}
    urls = render.render('index.html', vars_dict).encode('latin-1', 'replace')
    return urls

def content_html():
    html = render.render('content.html').encode('latin-1', 'replace')
    return html

def file_html():
    # html = render.render('file.html').encode('latin-1', 'replace')
    html = 'This is a plain text document.'
    return html

def image_html():
    fp = open('./images/justin_eli.jpg', 'rb')
    data = fp.read()
    fp.close()

    html = render.render('image.html').encode('latin-1', 'replace')
    return data 

def form_html():
    vars_dict = {'submit_url': '/submit'}
    html = render.render('form.html', vars_dict).encode('latin-1', 'replace')
    return html

def submit_html(environ):
    query = environ['QUERY_STRING']

    html = ''
    res = urlparse.parse_qs(query)
    if len(res) < 2: # check if the input was valid
        html = render.render('error.html').encode('latin-1', 'replace')
    else:
        vars_dict = {'firstname': res['firstname'][0], 
            'lastname': res['lastname'][0]}
        html = render.render('submit.html', vars_dict).encode('latin-1', 'replace')

    return html

def urlencoded_html(form):
# query_string = environ['QUERY_STRING']

    if 'firstname' not in form or 'lastname' not in form:
        html = render.render('error.html').encode('latin-1', 'replace')
    else:
        vars_dict = {'firstname': form['firstname'].value,\
            'lastname': form['lastname'].value}
        html = render.render('urlencoded.html', vars_dict).encode('latin-1', 'replace')

    return html

def multipart_html(form):
    html = render.render('multipart.html').encode('latin-1', 'replace')
    return html
    # TODO: print 'form: ', form['files'].value

def send_404_html():
    return '404 Not Found'

def error_html():
    html = render.render('error.html').encode('latin-1', 'replace')
    return html
    
# def handle_get(path, conn):
def handle_get(environ, headers):
    if environ['PATH_INFO'] == '/':
        return index_html()
    elif environ['PATH_INFO'] == '/content':
        return content_html()
    elif environ['PATH_INFO'] == '/file':
        headers[0] = ('Content-type', 'text/plain')
        return file_html()
    elif environ['PATH_INFO'] == '/image':
        headers[0] = ('Content-type', 'image/jpg')
        return image_html()
    elif environ['PATH_INFO'] == '/form':
        return form_html()
    elif environ['PATH_INFO'] == '/formPost':
        return form_post_html()
    elif environ['PATH_INFO'] == '/formPostMultipart':
        return form_post_multipart_html(environ)
    elif environ['PATH_INFO'].startswith('/submit'):
        return submit_html(environ)
    else:
        return send_404_html()

# --------------------------------------------------------------------------------
#                                  Posts
# --------------------------------------------------------------------------------

def form_post_html():
    vars_dict = {'submit_url': '/submit'}

    html = render.render('form_post.html', vars_dict).encode('latin-1', 'replace')
    return html

def form_post_multipart_html(form):
    vars_dict = {'submit_url': '/submit'}

    html = render.render('form_post_multipart.html', vars_dict).encode('latin-1', 'replace')
    return html
    # TODO: print 'form: ', form['files'].value

def handle_post(environ):
    headers = {}
    for k in environ.keys():
        headers[k.lower()] = environ[k]

    form = cgi.FieldStorage(headers=headers, fp=environ['wsgi.input'],\
            environ=environ)

    print 'form: ', form

    if 'application/x-www-form-urlencoded' in environ['CONTENT_TYPE']:
        return urlencoded_html(form)
    elif 'multipart/form-data;' in environ['CONTENT_TYPE']:
        return multipart_html(form)
    else:
        return error_html()

# from http://docs.python.org/2/library/wsgiref.html

# referenced bjurgess1
# A relatively simple WSGI application. It's going to print out the
# environment dictionary after being updated by setup_testing_defaults
def simple_app(environ, start_response):
    setup_testing_defaults(environ)

    status = '200 OK'
    headers = [('Content-type', 'text/html')]
    response = ''

    if environ['REQUEST_METHOD'] == 'GET':
        response = handle_get(environ, headers)
    elif environ['REQUEST_METHOD'] == 'POST':
        response = handle_post(environ)

    start_response(status, headers)
    return [response]

def make_app():
    return simple_app
