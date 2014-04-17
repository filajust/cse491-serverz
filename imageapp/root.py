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
        return html.render('index.html')

    @export(name='upload')
    def upload(self):
        return html.render('upload.html')

    @export(name='view_comments')
    def view_comments(self):
        img = image.get_latest_image()
        res = image.get_comments(img)
        return res

    @export(name='add_comment')
    def add_comment(self):
        request = quixote.get_request()
        comment = request.form['comment'].encode("latin-1")

        img = image.get_latest_image()
        img = image.add_comment(img, comment)
        imageapp_sql.update(img)
        return html.render('index.html')

    @export(name='upload_receive')
    def upload_receive(self):
        request = quixote.get_request()
        # print 'request.form.keys(): ', request.form.keys()

        the_file = request.form['file']
        # print dir(the_file)
        # print 'received file with name:', the_file.base_filename
        data = the_file.read(int(1e9))
        img = image.create_image_dict(data = data,\
                fileName = the_file.base_filename,\
                description = "uploaded image")
        image.add_image(img, 'png')

        # datatype = the_file.base_filename.split('.')[-1]
        # image.add_image(data, 'png')
        return html.render('index.html')
        # TODO: actually redirect
        # return quixote.redirect('http://localhost:9567')

    @export(name='image')
    def image(self):
        return html.render('image.html')

    @export(name='image_list')
    def image_list(self):
        image_num = image.get_image_num()
        vars_dict = {'num_images': image_num}
        return html.render('image_list.html', vars_dict)

    @export(name='image_list_server_side_thumbnail')
    def image_list_server_side_thumbnail(self):
        image_num = image.get_image_num()
        vars_dict = {'num_images': image_num}
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

        vars_dict = {'description': img['description'],
                     'commentList': img['commentList'],
                     'thumbnail': img['thumbnail'],
                     'file_name': img['file_name']}
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
