import os
import quixote
from quixote.directory import Directory, export, subdir
from quixote.util import StaticDirectory
from . import html, image, imageapp_sql

class RootDirectory(Directory):
    _q_exports = ['static']
    static = StaticDirectory(os.path.join(os.path.dirname(__file__),'static'))

    @export(name='')                    # this makes it public.
    def index(self):
        username = quixote.get_cookie('username')
        vars_dict = {'username': ''}
        if username:
            vars_dict = {'username': username}

        return html.render('index.html', vars_dict)

    # TODO: why do I need to do this
    @export(name='index')                    # this makes it public.
    def index_backup(self):
        username = quixote.get_cookie('username')
        vars_dict = {'username': ''}
        if username:
            vars_dict = {'username': username}

        return html.render('index.html', vars_dict)

    @export(name='upload')
    def upload(self):
        username = quixote.get_cookie('username')
        vars_dict = {'username': ''}
        if username:
            vars_dict = {'username': username}

        return html.render('upload.html', vars_dict)

    @export(name='view_comments')
    def view_comments(self):
        img = image.get_latest_image()
        res = image.get_comments(img)
        return res

    def set_cookie(self, username):
                quixote.get_response().set_cookie('username', username)

    @export(name='add_comment')
    def add_comment(self):
        request = quixote.get_request()
        comment = request.form['comment'].encode("latin-1")

        img = image.get_latest_image()
        img = image.add_comment(img, comment)
        imageapp_sql.update(img)

        username = quixote.get_cookie('username')
        vars_dict = {'username': ''}
        if username:
            vars_dict = {'username': username}

        return html.render('index.html', vars_dict)

    @export(name='create_account_page')
    def create_account_page(self):
        username = quixote.get_cookie('username')
        vars_dict = {'username': ''}
        if username:
            vars_dict = {'username': username}

        return html.render('create_account.html', vars_dict)

    @export(name='login_page')
    def login_page(self):
        username = quixote.get_cookie('username')
        vars_dict = {'username': ''}
        if username:
            vars_dict = {'username': username}

        return html.render('login.html', vars_dict)

    @export(name='create_user')
    def create_account(self):
        request = quixote.get_request()

        username = request.form['username'].encode("latin-1")
        password = request.form['password'].encode("latin-1")
        password_confirm = request.form['password_confirm'].encode("latin-1")

        vars_dict = {'username': ''}
        if password and password_confirm and username:
            if password == password_confirm:
                imageapp_sql.create_user(username, password)
                vars_dict = {'username': username}
                self.set_cookie(username)
        
        return html.render('index.html', vars_dict)

    @export(name='login')
    def login(self):
        request = quixote.get_request()

        authenticated = False
        username = request.form['username'].encode("latin-1")
        password = request.form['password'].encode("latin-1")
        if password and username:
            authenticated = imageapp_sql.authenticate(username, password)
        
        vars_dict = {'username': ''}
        if authenticated:
            vars_dict = {'username': username}
            self.set_cookie(username)

        return html.render('index.html', vars_dict)

    @export(name='upload_receive')
    def upload_receive(self):
        request = quixote.get_request()
        # print 'request.form.keys(): ', request.form.keys()
        username = quixote.get_cookie('username')

        the_file = request.form['file']
        # print dir(the_file)
        # print 'received file with name:', the_file.base_filename
        data = the_file.read(int(1e9))
        img = image.create_image_dict(data = data,\
                fileName = the_file.base_filename,\
                description = "uploaded image",\
                user = username)
        image.add_image(img, 'png')

        vars_dict = {'username': ''}
        if username:
            vars_dict = {'username': username}

        return html.render('index.html', vars_dict)
        # TODO: actually redirect
        # return quixote.redirect('http://localhost:9567')

    @export(name='image')
    def image(self):
        username = quixote.get_cookie('username')
        vars_dict = {'username': ''}
        if username:
            vars_dict = {'username': username}

        return html.render('image.html', vars_dict)

    @export(name='image_list')
    def image_list(self):
        image_num = image.get_image_num()
        vars_dict = {'num_images': image_num}

        username = quixote.get_cookie('username')
        vars_dict['username'] = ''
        if username:
            vars_dict['username'] = username

        return html.render('image_list.html', vars_dict)

    @export(name='image_list_server_side_thumbnail')
    def image_list_server_side_thumbnail(self):
        image_num = image.get_image_num()
        vars_dict = {'num_images': image_num}

        username = quixote.get_cookie('username')
        vars_dict['username'] = ''
        if username:
            vars_dict['username'] = username

        return html.render('image_list_server_side_thumbnail.html', vars_dict)

    @export(name='image_raw')
    def image_raw(self):
        response = quixote.get_response()
        request = quixote.get_request()

        image_num = None
        item = None
        if 'num' in request.form.keys():
            try:
                image_num = int(request.form['num'].encode("ascii"))
            except ValueError:
                print "ERROR: not an int... showing latest"
                image_num = image.get_image_num()
            image_count = image.get_image_num()

            if image_num > image_count:
                image_num = image_count 
            elif image_num < 0:
                image_num = 0

            item = image.get_image(image_num)
        elif 'special' in request.form.keys():
            special = request.form['special'].encode("latin-1")
            if special == 'latest':
                item = image.get_latest_image()
            else:
                # TODO: different case for this?
                item = image.get_latest_image()
        else:
            # TODO: different case for this?
            item = image.get_latest_image()

        # TODO: set content_type needs correct data type
        if item:
            ext = item['file_name'].split('.')[1]
            response.set_content_type(ext)
            return item['data'] 
        else:
            return None

    @export(name='retrieve_metadata')
    def retrieve_metadata(self):
        request = quixote.get_request()

        image_num = None
        item = None
        if 'num' in request.form.keys():
            try:
                image_num = int(request.form['num'].enclode("ascii"))
            except ValueError:
                print "ERROR: not an int... showing latest metadata"
                image_num = image.get_image_num()
        else:
            image_num = image.get_image_num() - 1

        image_count = image.get_image_num()

        if image_num > image_count:
            image_num = image_count
        elif image_num < 0:
            image_num = 0

        img = image.get_image(image_num)

        username = quixote.get_cookie('username')
        if username == None:
            username = ''
        vars_dict = {'description': img['description'],
                     'commentList': img['commentList'],
                     'thumbnail': img['thumbnail'],
                     'file_name': img['file_name'],
                     'user' : img['user'],
                     'username' : username}
        return html.render('retrieve_metadata.html', vars_dict)
        

    @export(name='image_raw_thumbnail')
    def image_raw_thumbnail(self):
        response = quixote.get_response()
        request = quixote.get_request()

        image_num = None
        item = None
        if 'num' in request.form.keys():
            try:
                image_num = int(request.form['num'].encode("ascii"))
            except ValueError:
                print "ERROR: not an int... showing latest"
                image_num = image.get_image_num()
            
            image_count = image.get_image_num()

            if image_num > image_count:
                image_num = image_count 
            elif image_num < 0:
                image_num = 0

            item = image.get_image(image_num)
        elif 'special' in request.form.keys():
            special = request.form['special'].encode("latin-1")
            if special == 'latest':
                item = image.get_latest_image()
            else:
                # TODO: different case for this?
                item = image.get_latest_image()
        else:
            # TODO: different case for this?
            item = image.get_latest_image()

        # TODO: set content_type needs correct data type
        if item:
            ext = item['file_name'].split('.')[1]
            response.set_content_type(ext)
            return item['thumbnail'] 
        else:
            return None
