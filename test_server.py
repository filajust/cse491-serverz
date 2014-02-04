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
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = \
            'HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n\r\n' + \
            '<h1>Hello, world.</h1>This is filajust\'s Web server.\r\n\r\n\
            <p><a href="/content">Content</a></p>\
            <p><a href="/file">File</a></p>\
            <p><a href="/image">Image</a></p>\
            <p><a href="/form">Form</a></p>\
            <p><a href="/formPost">Form (post)</a></p>'\

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_to_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return = \
            'HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n\r\n' + \
            '<p>Content</p>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_to_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = \
            'HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n\r\n' + \
            '<p>Image</p>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_to_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    expected_return = \
            'HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n\r\n' + \
            '<p>File</p>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_post_request():
    conn = FakeConnection("POST / HTTP/1.0/r/n/r/n")
    expected_return = \
            'HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n\r\n' + \
            '<h1>Server Error</h1>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_submit_post():
    conn = FakeConnection("POST /submit HTTP/1.0\r\n\r\n\
            From: test@testy.com\
            User-Agent: HTTPTool/1.0\
            Content-Type: application/x-www-form-urlencoded\
            Content-Length\n" + \
            "firstname=Test&lastname=Testing")
    expected_return = \
                   'HTTP/1.0 200 OK\r\n' + \
                   'Content-type: text/html\r\n\r\n' + \
                   '<p>Hello Mr. Test Testing, thank you for using a post \
                    request</p>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_submit_get():
    conn = FakeConnection("GET /submit?firstname=Test&lastname=Testing \
            HTTP/1.0\r\n\r\n")
    
    expected_return = \
               'HTTP/1.0 200 OK\r\n' + \
               'Content-type: text/html\r\n\r\n' + \
               '<p>Hello Mr. Test Testing</p>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_form_get():
    conn = FakeConnection("GET /form HTTP/1.0\r\n\r\n")
    expected_return = \
        'HTTP/1.0 200 OK\r\n' + \
        'Content-type: text/html\r\n\r\n' + \
        '<p>Please fill in name</p>\
        <form action=\'/submit\' method=\'GET\'>\
        First Name: <input type=\'text\' name=\'firstname\'>\
        Last Name: <input type=\'text\' name=\'lastname\'>\
        <input type=\'submit\' value=\'Submit\'>\
        </form>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)
