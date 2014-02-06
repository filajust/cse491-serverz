import server

class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r
            
        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def close(self):
        self.is_closed = True

# Test a basic GET call.
def test_handle_connection():
    conn = FakeConnection("GET / HTTP/1.0\r\n\ \
            \r\n\r\n")
    expected_return = \
    'HTTP/1.0 200 OK\r\n' + \
    'Content-type: text/html\r\n\r\n' + \
    '<h1>Hello, world.</h1>\n\n' + \
    'This is filajust\'s Web server.\n\n' + \
    '<p><a href="/content">Content</a></p>\n' + \
    '<p><a href="/file">File</a></p>\n' + \
    '<p><a href="/image">Image</a></p>\n' + \
    '<p><a href="/form">Form</a></p>\n' + \
    '<p><a href="/formPost">Form (post)</a></p>\n' + \
    '<p><a href="/formPostMultipart">Form (post multipart)</a></p>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_to_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n \
            \r\n\r\n")
    expected_return = \
    'HTTP/1.0 200 OK\r\n' + \
    'Content-type: text/html\r\n\r\n' + \
    '<p>Content</p>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_to_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n \
            \r\n\r\n")
    expected_return = \
    'HTTP/1.0 200 OK\r\n' + \
    'Content-type: text/html\r\n\r\n' + \
    '<p>Image</p>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_to_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n \
            \r\n\r\n")
    expected_return = \
    'HTTP/1.0 200 OK\r\n' + \
    'Content-type: text/html\r\n\r\n' + \
    '<p>File</p>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

    '''
def test_handle_error_post_request():
    conn = FakeConnection("POST / HTTP/1.0\r\n \
            \r\n\r\n")
    expected_return = \
    'HTTP/1.0 200 OK\r\n' + \
    'Content-type: text/html\r\n\r\n' + \
    '<h1>Error</h1>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)
    '''

def test_handle_urlencoded_post():
    conn = FakeConnection("POST /submit HTTP/1.0\r\n" + \
            "From: test@testy.com\n" + \
            "User-Agent: HTTPTool/1.0\n" + \
            "Content-Type: application/x-www-form-urlencoded\n" + \
            "Content-Length: 31\r\n\r\n" + \
            "firstname=Test&lastname=Testing")
    expected_return = \
    'HTTP/1.0 200 OK\r\n' + \
    'Content-type: text/html\r\n\r\n' + \
    '<p>Hello Mr. Test Testing, thank you for using a post' +  \
    ' request</p>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_multipart_post():
    conn = FakeConnection("POST /submit HTTP/1.0\r\n" + \
            "From: test@testy.com\n" + \
            "User-Agent: HTTPTool/1.0\n" + \
            "Content-Type: multipart/form-data; boundary=---------------------------55261788821295539881451415414\n" + \
            "Content-Length: 3373\r\n\r\n" + \
            "-----\n" + \
            "content:  ------------------------55261788821295539881451415414\n" + \
            "Content-Disposition: form-data; name=\"files\"; filename=\"Astronaut.png\"\n" + \
            "Content-Type: image/png")

    expected_return = \
    'HTTP/1.0 200 OK\r\n' + \
    'Content-type: text/html\r\n\r\n' + \
    '<h1>multipart</h1>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_submit_get():
    conn = FakeConnection("GET /submit?firstname=Test&lastname=Testing \
            HTTP/1.0\r\n\
            \r\n\r\n")
    
    expected_return = \
    'HTTP/1.0 200 OK\r\n' + \
    'Content-type: text/html\r\n\r\n' + \
    '<p>Hello Mr. Test Testing</p>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_form_get():
    conn = FakeConnection("GET /form HTTP/1.0\r\n\ \
            \r\n\r\n")
    expected_return = \
    'HTTP/1.0 200 OK\r\n' + \
    'Content-type: text/html\r\n\r\n' + \
    '<p>Please fill in name</p>\n' + \
    '<form action=\'/submit\' method=\'GET\'>\n' + \
    '    First Name: <input type=\'text\' name=\'firstname\'>\n' + \
    '    Last Name: <input type=\'text\' name=\'lastname\'>\n' + \
    '    <input type=\'submit\' value=\'Submit\'>\n' + \
    '</form>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

