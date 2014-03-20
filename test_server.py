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
    conn = FakeConnection("GET / HTTP/1.0\r\n \
            \r\n\r\n")
    partial_expected_return = 'HTTP/1.0 200 OK'

    server.handle_connection(conn, 'imageapp')

    assert partial_expected_return in conn.sent, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_to_upload_hw7():
    conn = FakeConnection("GET /upload HTTP/1.0\r\n \
            \r\n\r\n")
    
    status = 'HTTP/1.0 200 OK'
    partial_expected_return = 'Upload'

    server.handle_connection(conn, 'imageapp')

    assert status in conn.sent, 'Got: %s' % (repr(conn.sent),)
    assert partial_expected_return in conn.sent, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_to_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n \
            \r\n\r\n")
    status = 'HTTP/1.0 200 OK'
    partial_expected_return = 'Content'

    server.handle_connection(conn, 'myapp')

    assert status in conn.sent, 'Got: %s' % (repr(conn.sent),)
    assert partial_expected_return in conn.sent, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_to_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n \
            \r\n\r\n")

    status = 'HTTP/1.0 200 OK'
    partial_expected_return = 'Content-type: image/jpg'

    server.handle_connection(conn, 'myapp')

    assert status in conn.sent, 'Got: %s' % (repr(conn.sent),)
    assert partial_expected_return in conn.sent, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_to_image_hw7():
    conn = FakeConnection("GET /image HTTP/1.0\r\n \
            \r\n\r\n")
    status = 'HTTP/1.0 200 OK'
    partial_expected_return = 'image'

    server.handle_connection(conn, 'imageapp')

    assert status in conn.sent, 'Got: %s' % (repr(conn.sent),)
    assert partial_expected_return in conn.sent, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_to_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n \
            \r\n\r\n")
    status = 'HTTP/1.0 200 OK'
    partial_expected_return = 'Content-type: text/plain'

    server.handle_connection(conn, 'myapp')

    assert status in conn.sent, 'Got: %s' % (repr(conn.sent),)
    assert partial_expected_return in conn.sent, 'Got: %s' % (repr(conn.sent),)

'''
def test_handle_error_post_request():
    conn = FakeConnection("POST / HTTP/1.0\r\n \
            \r\n\r\n")
    status = 'HTTP/1.0 200 OK'
    partial_expected_return = 'Error'

    server.handle_connection(conn, 'myapp')

    assert status in conn.sent, 'Got: %s' % (repr(conn.sent),)
    assert partial_expected_return in conn.sent, 'Got: %s' % (repr(conn.sent),)
'''

def test_handle_urlencoded_post():
    conn = FakeConnection("POST /submit HTTP/1.0\r\n" + \
            "From: test@testy.com\n" + \
            "User-Agent: HTTPTool/1.0\n" + \
            "Content-Type: application/x-www-form-urlencoded\n" + \
            "Content-Length: 31\r\n\r\n" + \
            "firstname=Test&lastname=Testing")
    status = 'HTTP/1.0 200 OK'
    partial_expected_return = 'Test Testing'

    server.handle_connection(conn, 'myapp')

    assert status in conn.sent, 'Got: %s' % (repr(conn.sent),)
    assert partial_expected_return in conn.sent, 'Got: %s' % (repr(conn.sent),)

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

    status = 'HTTP/1.0 200 OK'
    partial_expected_return = 'Multipart'

    server.handle_connection(conn, 'myapp')

    assert status in conn.sent, 'Got: %s' % (repr(conn.sent),)
    assert partial_expected_return in conn.sent, 'Got: %s' % (repr(conn.sent),)

def test_handle_submit_get():
    conn = FakeConnection("GET /submit?firstname=Test&lastname=Testing HTTP/1.0\r\n \r\n\r\n")
    
    status = 'HTTP/1.0 200 OK'
    partial_expected_return = 'Test Testing'

    server.handle_connection(conn, 'myapp')

    assert status in conn.sent, 'Got: %s' % (repr(conn.sent),)
    assert partial_expected_return in conn.sent, 'Got: %s' % (repr(conn.sent),)

def test_handle_form_get():
    conn = FakeConnection("GET /form HTTP/1.0\r\n\n\r\n\r\n")

    partial_expected_return = '<form action=\'/submit\''
    status = 'HTTP/1.0 200 OK'

    server.handle_connection(conn, 'myapp')

    assert status in conn.sent, 'Got: %s' % (repr(conn.sent),)
    assert partial_expected_return in conn.sent, 'Got: %s' % (repr(conn.sent),)

'''
def test_handle_altdemo():
    conn = FakeConnection("GET / HTTP/1.0\r\n\n\r\n\r\n")

    status = 'HTTP/1.0 200 OK'
    partial_expected_return = 'Quixote Session'

    server.reset_connection()
    server.handle_connection(conn, 'altdemoapp')

    assert status in conn.sent, 'Got: %s' % (repr(conn.sent),)
    assert partial_expected_return in conn.sent, 'Got: %s' % (repr(conn.sent),)
'''
